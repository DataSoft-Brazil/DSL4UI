from utils.generator_utils import WEB_FOLDER_NAME

run_content = f'''from {WEB_FOLDER_NAME} import app

app.run(host='0.0.0.0', port='5000', debug=True)
'''


def generate_web_init_content(dsl_app):
    # login_manager = dsl_app['login_manager'] if 'login_manager' in dsl_app else None
    main_db = dsl_app['db']['main']
    alternative_dbs = dsl_app['db'].copy()
    del alternative_dbs['main']
    init_content = '''# from db import get_db_uri_from_env
# from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
# api_restful = Api(app)

app.config["SECRET_KEY"] = "36f751563a37902a7c5a3e2f067f625c"
'''
    init_content += f'''
app.config["SQLALCHEMY_DATABASE_URI"] = "{main_db}"'''
    if alternative_dbs:
        init_content += f'''
app.config["SQLALCHEMY_BINDS"] = {alternative_dbs}'''

    init_content += '''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"max_identifier_length": 30}
app.config['LOGIN_DISABLED'] = False
db = SQLAlchemy(app)

# import web_app.login_manager

# import web_app.api.routes_api\n'''
    init_content += f'import {WEB_FOLDER_NAME}.routes\n'
    return init_content


def generate_web_routes_content(dsl_app):
    app_title = dsl_app['title'] if 'title' in dsl_app else 'Default'
    routes_content = f'''# from flask_login import login_user, login_required, logout_user, current_user
# from db.data_access_objects import Usuario
# from utils.utils_crypt import check_hash
# from {WEB_FOLDER_NAME}.forms import LoginForm
from flask import render_template, flash, redirect, request
from utils.flask_utils import url_for
from utils.sql_utils import parse_sql_db_key_and_query
from {WEB_FOLDER_NAME} import app, db


@app.route("/")
@app.route("/home")
# @login_required
def home():
    # usuario=current_user
    return render_template("home.html", title="Home - {app_title}")


#@app.route("/login", methods=['GET', 'POST'])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#        usuario = Usuario.read_by_email(form.email.data)
#        if usuario and check_hash(form.senha.data, usuario.senha_hash):
#            login_user(usuario, remember=False)
#            flash('Login feito com sucesso.', 'success')
#            return redirect(request.args.get("next") or url_for("home"))
#        else:
#            flash('E-mail ou senha inválida. Certifique-se de preencher as credenciais corretas.', 'danger')
#    return render_template('login.html', title='Login', form=form)


#@app.route("/logout")
#@login_required
#def logout():
#    logout_user()
#    return redirect(url_for("login"))
'''
    for route in dsl_app['routes']:
        template_name = route['endpoint'][1:].replace('/', '_')
        route_title = route.get('title') or ''
        select_options = ''
        routes_content += f'''\n
@app.route("{route['endpoint']}")
# @login_required
def {template_name}():'''
        if 'inputs' in route:
            for input_field in route['inputs']:
                if 'select' in input_field:
                    label = input_field['label']
                    select_options_listname = f'select_{label.lower().replace(" ", "_")}_options'
                    select_options_currentname = f'select_{label.lower().replace(" ", "_")}_current'
                    select_options += f', {select_options_listname}={select_options_listname}, {select_options_currentname}={select_options_currentname}'
                    routes_content += f'''
    db_key, query = parse_sql_db_key_and_query('{input_field['select']}')
    if db_key is not None:
        if db_key == 'main':
            q_result = db.session.execute(query)
        else:
            q_result = db.session.execute(query, bind=db.get_engine(app, f'{{db_key}}'))
    {select_options_listname} = []
    for row in q_result:
        {select_options_listname}.append((row[0], row[1]))
    {select_options_currentname} = {select_options_listname}[0][0]
'''
        routes_content += f'''
    return render_template("{template_name}.html", title="{route_title} - {app_title}"{select_options})\n'''
    return routes_content


flask_utils_content = '''from flask import url_for as url_for_original

def url_for(endpoint, **values):
    url = url_for_original(endpoint, **values)
    return url[1:]
'''

sql_utils_content = r'''
import re

def parse_sql_db_key_and_query(text):
    match = re.findall(r'[fF]rom (.*?)\.', text)
    if match:
        query = 'SELECT id, ' + text.replace(match[0] + '.', '')
        return match[0], query
    else:
        return None, None
'''