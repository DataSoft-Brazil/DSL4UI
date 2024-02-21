import unicodedata
import os
import re


def sanitize_filename(filename):
    val = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\W+', '_', val)


def create_file(start_path, file_name, file_extension, content):
    file_name = sanitize_filename(file_name)
    path = os.path.join(start_path, f'{file_name}.{file_extension}')
    with open(path, 'x') as f:
        f.write(content)


def create_folder(start_path, folder_name):
    folder_name = sanitize_filename(folder_name)
    path = os.path.join(start_path, folder_name)
    os.mkdir(path)


def create_folders(start_path, folders_names):
    for folder_name in folders_names:
        create_folder(start_path, folder_name)


def create_folder_hierarchy(start_path, folder_hierarchy):
    folder_hierarchy = sanitize_filename(folder_hierarchy)
    path = os.path.join(start_path, folder_hierarchy)
    os.makedirs(path)
