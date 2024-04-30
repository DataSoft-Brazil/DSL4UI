from utils.generator_utils import WEB_FOLDER_NAME, parse_sql_db_key_and_query

run_content = f'''from {WEB_FOLDER_NAME} import create_app

create_app().run(port='5000', debug=False, ssl_context='adhoc')
'''

user_model_content = '''class User:
    def __init__(self, login, name, email):
        self.login = login
        self.name = name
        self.email = email

    def is_active(self):
        return True

    def get_id(self):
        return self.login

    def is_authenticated(self):
        return True
'''


def generate_web_init_content(dsl_app):
    imports = ''
    consts_and_variables = '\n'
    app_function = '\n'
    app_login_manager = '\n'
    login_manager = dsl_app['login_manager'] if 'login_manager' in dsl_app else {}
    if 'type' in login_manager and login_manager['type'] == 'oauth2@google.com':
        imports += '''from flask_login import LoginManager, login_user, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient\n'''
        consts_and_variables += f'''GOOGLE_CLIENT_ID = "{login_manager['client_id']}"
GOOGLE_CLIENT_SECRET = "{login_manager['client_secret']}"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"\n'''
        app_login_manager += "" '''
    login_manager = LoginManager()
    login_manager.login_view = WEBAPP_BASE_URI + "login"
    login_manager.login_message = ""
    login_manager.init_app(app)
    client = WebApplicationClient(GOOGLE_CLIENT_ID)

    from .user_model import User
    
    users_dict = {}

    @login_manager.user_loader
    def load_user(user_id):
        return users_dict[user_id] if user_id in users_dict else None

    def get_google_provider_cfg():
        return requests.get(GOOGLE_DISCOVERY_URL).json()

    @app.route(ROOT_CONTEXT_PATH + "/login")
    def login():
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        state = request.args.get('next')
        if state:
            state = external_uri(state, WEBAPP_BASE_URI, request)
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=WEBAPP_BASE_URI + "login/callback",
            scope=["openid", "email", "profile"],
            state=state
        )
        return redirect(request_uri)

    @app.route(ROOT_CONTEXT_PATH + "/login/callback")
    def callback():
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=external_uri(request.url, WEBAPP_BASE_URI, request),
            redirect_url=external_uri(request.base_url, WEBAPP_BASE_URI, request),
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )
        client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            # picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            flash("User email not available or not verified by Google.", "danger")
            return redirect(url_for("bp_basic.home", base=WEBAPP_BASE_URI))
        user = User(
            login=unique_id, name=users_name, email=users_email
        )
        login_user(user)
        if user.login not in users_dict.keys():
            users_dict[user.login] = user
        next_uri = request.args.get("state")
        return redirect(next_uri if next_uri else url_for("bp_basic.home", base=WEBAPP_BASE_URI))

    @app.route(ROOT_CONTEXT_PATH + '/logout')
    def logout():
        logout_user()
        return redirect(url_for('home'))
    '''
    # o nome "db1" (a conexão principal) é obrigatório na dsl, conexões adicionais com outros nomes são opcionais.
    main_db = dsl_app['db']['db1']
    alternative_dbs = dsl_app['db'].copy()
    del alternative_dbs['db1']
    imports += '''from utils.flask_utils import url_for, external_uri, WEBAPP_BASE_URI, ROOT_CONTEXT_PATH
from flask import Flask, flash, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
import logging
import json
import os'''
    consts_and_variables += '''db = None
__version__ = "0.1.0"'''
    app_function += f'''def create_app(test_config=None):
    app = Flask(__name__, static_url_path=ROOT_CONTEXT_PATH + '/static')
    app.jinja_env.globals.update(url_for=url_for)
    {app_login_manager}
    app.config["SECRET_KEY"] = "36f751563a37902a7c5a3e2f067f625c"
    app.config["SQLALCHEMY_DATABASE_URI"] = "{main_db}"
    {f'app.config["SQLALCHEMY_BINDS"] = {alternative_dbs}' if alternative_dbs else ''}
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {{"max_identifier_length": 30}}
    app.config['LOGIN_DISABLED'] = False
    global db
    db = SQLAlchemy(app)
    
    @app.errorhandler(Exception)
    def internal_server_error(e):
        logging.exception(e)
        return render_template('exception.html', e=e, title='Erro', user=current_user), 500
    
    from .routes import bp_basic

    app.register_blueprint(bp_basic, url_prefix=ROOT_CONTEXT_PATH)
    
    return app
'''
    return f'{imports}\n{consts_and_variables}\n{app_function}'


def generate_web_routes_content(dsl_app):
    app_title = dsl_app['title'] if 'title' in dsl_app else 'Default'
    imports = ''
    consts_and_variables = ''
    routes = ''
    imports += f'''from utils.sql_utils import parse_sql_db_key_and_query
from flask_login import current_user, login_required
from flask import Blueprint, render_template
from {WEB_FOLDER_NAME} import __version__, db
from utils.flask_utils import url_for
from sqlalchemy.sql import text'''
    consts_and_variables += '''bp_basic = Blueprint('bp_basic', __name__)'''
    routes += f'''
@bp_basic.route("/")
@bp_basic.route("/home")
def home():
    return render_template("home.html", title="Home - {app_title}", version=__version__, user=current_user)
'''
    for route in dsl_app['routes']:
        template_name = route['endpoint'][1:].replace('/', '_')
        login_required = ''
        login_manager = dsl_app['login_manager'] if 'login_manager' in dsl_app else {}
        if login_manager:
            login_required = '@login_required'
        route_title = route.get('title') or ''
        select_variables = ''
        table_variables = ''
        routes += f'''\n
@bp_basic.route("{route['endpoint']}")
{login_required}
def {template_name}():'''
        if 'inputs' in route:
            for input_field in route['inputs']:
                if 'select' in input_field:
                    label = input_field['label']
                    select_options_listname = f'select_{label.lower().replace(" ", "_")}_options'
                    select_options_currentname = f'select_{label.lower().replace(" ", "_")}_current'
                    select_variables += f', {select_options_listname}={select_options_listname}, {select_options_currentname}={select_options_currentname}'
                    routes += f'''
    db_key, query, fields = parse_sql_db_key_and_query("""{input_field['select']}""", 'select')
    if db_key is not None:
        if db_key == 'db1':
            q_result = db.session.execute(text(query))
        else:
            q_result = db.session.execute(text(query), bind=db.get_engine(app, f'{{db_key}}'))
    {select_options_listname} = []
    if q_result:
        for row in q_result:
            {select_options_listname}.append((row[0], row[1]))
    {select_options_currentname} = {select_options_listname}[0][0]
'''
                if 'table' in input_field:
                    label = input_field['label']
                    table_columns_listname = f'table_{label.lower().replace(" ", "_")}_columns'
                    table_rows_listname = f'table_{label.lower().replace(" ", "_")}_rows'
                    table_variables += f', {table_columns_listname}={table_columns_listname}, {table_rows_listname}={table_rows_listname}'
                    _, _, fields = parse_sql_db_key_and_query(input_field['table'], 'table')
                    routes += f'''
    db_key, query, fields = parse_sql_db_key_and_query("""{input_field['table']}""", 'table')
    if db_key is not None:
        if db_key == 'db1':
            q_result = db.session.execute(text(query))
        else:
            q_result = db.session.execute(text(query), bind=db.get_engine(app, f'{{db_key}}'))
    print(fields)
    {table_columns_listname} = fields
    {table_rows_listname} = []
    if q_result:
        for row in q_result:
            {table_rows_listname}.append(({', '.join(["row[" + str(i) + "]" for i in range(0,len(fields))])}))
'''
        routes += f'''
    return render_template("{template_name}.html", title="{route_title} - {app_title}"{select_variables}{table_variables})\n'''
    return f'{imports}\n{consts_and_variables}\n{routes}'


flask_utils_content = '''from flask import url_for as url_for_original
import os

WEBAPP_BASE_URI = os.environ.get("WEBAPP_BASE_URI", "https://127.0.0.1:5000/")
ROOT_CONTEXT_PATH = os.environ.get("ROOT_CONTEXT_PATH", "")


def url_for(endpoint, base=None, **values):
    if len(ROOT_CONTEXT_PATH):
        return url_for_original(endpoint, **values)
    url = url_for_original(endpoint, **values)[1:]
    if base:
        return base + url
    return url


def external_uri(internal_uri, external_base, request):
    if ROOT_CONTEXT_PATH:
        context_path = ROOT_CONTEXT_PATH[1:]
        if not context_path.endswith('/'):
            context_path = context_path + '/'
    else:
        context_path = ''
    return internal_uri.replace(request.root_url + context_path, external_base)
'''

sql_utils_content = r'''import re

def parse_sql_db_key_and_query(text, input_type):
    db_key_match = re.findall(r'[fF]rom (.*?)\.', text)
    if db_key_match:
        db_key = db_key_match[0]
        infer_id_query = 'id, ' if input_type == 'select' else ''
        query = f'SELECT {infer_id_query}' + text.replace(db_key + '.', '')
        fields = []
        for field_match in re.findall(r'(.*?),|(.*)[fF]rom', text):
            field = field_match[0] or field_match[1]
            fields.append(field.strip())
        return db_key, query, fields
    else:
        return None, None, None
'''