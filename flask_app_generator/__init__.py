from utils.generator_utils import WEB_FOLDER_NAME, TEMPLATES_FOLDER_NAME, STATIC_FOLDER_NAME, CSS_FOLDER_NAME, \
    JS_FOLDER_NAME, UTILS_FOLDER_NAME
from flask_app_generator.files_content import run_content, generate_web_init_content, generate_web_routes_content, \
    flask_utils_content, sql_utils_content, user_model_content
from template_generator import generate_layout_template, generate_home_template, generate_custom_template, \
    generate_custom_js, exception_template_content
from utils.file_utils import make_folder_hierarchy, make_folder, make_file
import yaml
import os

PYTHON_EXTENSION = 'py'
JS_EXTENSION = 'js'
CSS_EXTENSION = 'css'
HTML_EXTENSION = 'html'

root_path = input('** Gerador DSL4UI **\n\nQual o caminho raiz do Web app a ser gerado?\n')
web_path = os.path.join(root_path, WEB_FOLDER_NAME)
utils_path = os.path.join(root_path, UTILS_FOLDER_NAME)
templates_path = os.path.join(web_path, TEMPLATES_FOLDER_NAME)
static_path = os.path.join(web_path, STATIC_FOLDER_NAME)
css_path = os.path.join(static_path, CSS_FOLDER_NAME)
js_path = os.path.join(static_path, JS_FOLDER_NAME)

# procura dsl.yaml no diretório de trabalho atual, ou em uma pasta chamada "private"
if os.path.isfile(os.path.join(os.getcwd(), 'dsl.yaml')):
    with open(os.path.join(os.getcwd(), 'dsl.yaml'), 'r', encoding='UTF-8') as f:
        dsl = yaml.load(f.read(), yaml.CLoader)
elif os.path.isfile(os.path.join(os.getcwd(), 'private', 'dsl.yaml')):
    with open(os.path.join(os.getcwd(), 'private', 'dsl.yaml'), 'r', encoding='UTF-8') as f:
        dsl = yaml.load(f.read(), yaml.CLoader)
else:
    raise Exception("dsl.yaml not found on current working directory")
dsl_app = dsl['app']

print("\ngerando arquivos...\n")
make_folder_hierarchy(root_path, '')
make_file(root_path, 'run', PYTHON_EXTENSION, run_content)

# make folders /web, /utils
make_folder(root_path, [WEB_FOLDER_NAME, UTILS_FOLDER_NAME])
# make folders /web/templates, /web/static
make_folder(web_path, [TEMPLATES_FOLDER_NAME, STATIC_FOLDER_NAME])
# make folders /web/static/css, /web/static/js
make_folder(static_path, [CSS_FOLDER_NAME, JS_FOLDER_NAME])

# /web files
make_file(web_path, '__init__', PYTHON_EXTENSION, generate_web_init_content(dsl_app))
make_file(web_path, 'routes', PYTHON_EXTENSION, generate_web_routes_content(dsl_app))
make_file(web_path, 'user_model', PYTHON_EXTENSION, user_model_content)

# /utils files
make_file(utils_path, 'flask_utils', PYTHON_EXTENSION, flask_utils_content)
make_file(utils_path, 'sql_utils', PYTHON_EXTENSION, sql_utils_content)

# /web/templates files
make_file(templates_path, 'layout', HTML_EXTENSION, generate_layout_template(dsl_app))
make_file(templates_path, 'home', HTML_EXTENSION, generate_home_template(dsl_app))
make_file(templates_path, 'exception', HTML_EXTENSION, exception_template_content)

# /web/static/css files
make_file(css_path, 'main', CSS_EXTENSION, '')

# /web/static/js files
make_file(js_path, 'layout', JS_EXTENSION, '')
if 'routes' in dsl_app:
    for route in dsl_app['routes']:
        template_name = route['endpoint'][1:].replace('/', '_')
        make_file(templates_path, template_name, HTML_EXTENSION, generate_custom_template(route))
        if 'backend' in route:
            make_file(js_path, template_name, JS_EXTENSION, generate_custom_js(route))

print(f'\nWeb app "{dsl_app["title"] if "title" in dsl_app else "Default"}" gerado em {root_path}')
