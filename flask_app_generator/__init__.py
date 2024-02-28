from flask_app_generator.app_files_contents import run_content, generate_web_init_content, generate_web_routes_content, \
    flask_utils_content
from template_generator import generate_layout_template, generate_home_template
from utils.generator_utils import WEB_FOLDER, TEMPLATES_FOLDER, STATIC_FOLDER, CSS_FOLDER, JS_FOLDER, UTILS_FOLDER
from utils.file_utils import make_folder_hierarchy, make_folder, make_file
import yaml
import os

PYTHON_FILE = 'py'
JS_FILE = 'js'
CSS_FILE = 'css'
HTML_FILE = 'html'

app_root_path = input('Qual o caminho da raiz da aplicação?\n')
web_path = os.path.join(app_root_path, WEB_FOLDER)
utils_path = os.path.join(app_root_path, UTILS_FOLDER)
templates_path = os.path.join(web_path, TEMPLATES_FOLDER)
static_path = os.path.join(web_path, STATIC_FOLDER)
css_path = os.path.join(static_path, CSS_FOLDER)
js_path = os.path.join(static_path, JS_FOLDER)

if os.path.isfile(os.path.join(os.getcwd(), 'dsl.yaml')):
    with open(os.path.join(os.getcwd(), 'dsl.yaml'), 'r', encoding='UTF-8') as f:
        dsl = yaml.load(f.read(), yaml.CLoader)
elif os.path.isfile(os.path.join(os.getcwd(), 'private', 'dsl.yaml')):
    with open(os.path.join(os.getcwd(), 'private', 'dsl.yaml'), 'r', encoding='UTF-8') as f:
        dsl = yaml.load(f.read(), yaml.CLoader)
dsl_app = dsl['app']

make_folder_hierarchy(app_root_path, '')
make_file(app_root_path, 'run', PYTHON_FILE, run_content)
make_folder(app_root_path, [WEB_FOLDER, UTILS_FOLDER])

make_file(web_path, '__init__', PYTHON_FILE, generate_web_init_content(dsl_app))
make_file(web_path, 'routes', PYTHON_FILE, generate_web_routes_content(dsl_app))
make_file(utils_path, 'flask_utils', PYTHON_FILE, flask_utils_content())

make_folder(web_path, [TEMPLATES_FOLDER, STATIC_FOLDER])
make_file(templates_path, 'layout', HTML_FILE, generate_layout_template(dsl_app))
make_file(templates_path, 'home', HTML_FILE, generate_home_template(dsl_app))
make_folder(static_path, [CSS_FOLDER, JS_FOLDER])
make_file(css_path, 'main', CSS_FILE, '')
make_file(js_path, 'layout', JS_FILE, '')

print('App criado no caminho:', app_root_path)
