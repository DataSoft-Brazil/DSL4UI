import unicodedata
import os
import re


def sanitize_filename(filename):
    val = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\W+', '_', val)


def make_file(start_path, file_name, file_extension, content):
    file_name = sanitize_filename(file_name)
    path = os.path.join(start_path, f'{file_name}.{file_extension}')
    with open(path, 'x', encoding='UTF-8') as f:
        f.write(content)
        print('arquivo gerado -', path)


def make_folder(start_path, name_or_names):
    if isinstance(name_or_names, list):
        for folder_name in name_or_names:
            folder_name = sanitize_filename(folder_name)
            path = os.path.join(start_path, folder_name)
            os.mkdir(path)
    else:
        folder_name = sanitize_filename(name_or_names)
        path = os.path.join(start_path, folder_name)
        os.mkdir(path)


def make_folder_hierarchy(start_path, folder_hierarchy):
    folder_hierarchy = sanitize_filename(folder_hierarchy)
    os.makedirs(os.path.join(start_path, folder_hierarchy))
