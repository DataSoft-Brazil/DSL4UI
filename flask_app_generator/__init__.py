from utils.generator_utils import WEB_FOLDER_NAME, TEMPLATES_FOLDER_NAME, STATIC_FOLDER_NAME, CSS_FOLDER_NAME, \
    JS_FOLDER_NAME, UTILS_FOLDER_NAME
from flask_app_generator.app_files_contents import run_content, generate_web_init_content, generate_web_routes_content, \
    flask_utils_content
from template_generator import generate_layout_template, generate_home_template
from utils.file_utils import make_folder_hierarchy, make_folder, make_file
import yaml
import os

PYTHON_EXTENSION = 'py'
JS_EXTENSION = 'js'
CSS_EXTENSION = 'css'
HTML_EXTENSION = 'html'

root_path = input('Qual o caminho da raiz da aplicação?\n')
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

make_folder_hierarchy(root_path, '')
make_file(root_path, 'run', PYTHON_EXTENSION, run_content)
make_folder(root_path, [WEB_FOLDER_NAME, UTILS_FOLDER_NAME])

make_file(web_path, '__init__', PYTHON_EXTENSION, generate_web_init_content(dsl_app))
make_file(web_path, 'routes', PYTHON_EXTENSION, generate_web_routes_content(dsl_app))
make_file(utils_path, 'flask_utils', PYTHON_EXTENSION, flask_utils_content)

make_folder(web_path, [TEMPLATES_FOLDER_NAME, STATIC_FOLDER_NAME])
make_file(templates_path, 'layout', HTML_EXTENSION, generate_layout_template(dsl_app))
make_file(templates_path, 'home', HTML_EXTENSION, generate_home_template(dsl_app))
make_folder(static_path, [CSS_FOLDER_NAME, JS_FOLDER_NAME])
make_file(css_path, 'main', CSS_EXTENSION, '')
make_file(js_path, 'layout', JS_EXTENSION, '')

print('App criado no caminho:', root_path)
