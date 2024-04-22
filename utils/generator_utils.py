import re

WEB_FOLDER_NAME = 'web'
TEMPLATES_FOLDER_NAME = 'templates'
STATIC_FOLDER_NAME = 'static'
CSS_FOLDER_NAME = 'css'
JS_FOLDER_NAME = 'js'
UTILS_FOLDER_NAME = 'utils'


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
