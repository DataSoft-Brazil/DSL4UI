from utils.file_utils import create_folder_hierarchy, create_folder, create_file
import os

app_root_path = input('Qual o caminho da raiz da aplicação?\n')
web_app_path = os.path.join(app_root_path, 'web_app')

# gerar pasta web_app com __init__.py e routes.py
create_folder_hierarchy(app_root_path, '')
create_folder(app_root_path, 'web_app')
create_file(web_app_path, '__init__', 'py', "Hello World")
create_file(web_app_path, 'routes', 'py', "Hello Routes")

print('App criado no caminho:', app_root_path)
