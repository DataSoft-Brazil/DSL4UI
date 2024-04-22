def generate_layout_template(dsl_app):
    app_title = dsl_app.get('title') or 'Default'
    app_theme = dsl_app['theme'] if 'theme' in dsl_app else 'light'
    layout_content = '<!DOCTYPE html>\n'
    layout_content += f'<html lang="pt-br" data-bs-theme="{app_theme}">\n\t'
    layout_content += '''<head>
            <meta charset="UTF-8">
            <title>{{title}} · Web App</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" type="image/x-icon" href="{{url_for('static', filename='img/favicon.ico')}}">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css" rel="stylesheet">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css"
                  rel="stylesheet" crossorigin="anonymous"
                  integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ">
            <link rel="stylesheet" type="text/css" href="{{url_for('static', filename='css/main.css')}}">
        </head>
        <body style="min-height: 100vh;">
            <header class="fluid-container">
                <nav class="navbar navbar-expand-lg bg-body-tertiary">
                    <div class="container-fluid">
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                                aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                            <div class="navbar-nav">\n\t\t\t\t\t\t\t'''
    layout_content += f'''<a class="nav-link active" href="{{{{ url_for('home') }}}}">{app_title}</a>\n\t\t\t\t\t\t\t'''
    for route in dsl_app['routes']:
        template_name = route['endpoint'][1:].replace('/', '_')
        route_title = route.get('title') or ''
        layout_content += f'''<a class="nav-link" href="{{{{ url_for('{template_name}') }}}}">{route_title}</a>\n\t\t\t\t\t\t\t'''
    layout_content += '''\n\t\t\t\t\t\t</div>
                        </div>
                    </div>
                </nav>
            </header>
            {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
            {% for category, message in messages %}
            <div class="row mx-2 justify-content-center">
                <div class="alert alert-{{ category }} mt-2 col-lg-7" role="alert">
                    {{ message }} <i class="fa-solid fa-xmark close-alert" data-bs-dismiss="alert" aria-label="Close"></i>
                </div>
            </div>
            {% endfor %}
            {% endif %}
            {% endwith %}
            <main class="m-3">
                {% block outside_container %}
                <div class="container">
                    {% block inside_container %}
                    {% endblock %}
                </div>
                {% endblock %}
            </main>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"
                    crossorigin="anonymous"
                    integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe">
            </script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/js/all.min.js"></script>
            <script src="https://code.jquery.com/jquery-3.7.0.min.js"
                    integrity="sha256-2Pmvv0kuTBOenSvLm6bvfBSSHrUJ+3A7x6P5Ebd07/g=" crossorigin="anonymous"></script>
            {% block scripts %}
            {% endblock %}
        </body>
    </html>'''
    return layout_content


def generate_home_template(dsl_app):
    app_title = dsl_app.get('title') or 'Default'
    home_content = '''{% extends "layout.html" %}

{% block inside_container %}\n'''
    home_content += f'<h1>{app_title}</h1>\n'
    home_content += '''{% endblock %}
'''
    return home_content


def generate_input_html(input_field):
    label = input_field['label']
    input_html = ''
    input_id = ''
    input_content = ''
    input_type = None
    if 'text' in input_field:
        input_type = 'text'
        input_id = input_field['text']
        input_html = f'''
    <label for="{input_id}" class="form-label">{label}</label>
    <input type="text" class="form-control" id="{input_id}">
'''
    elif 'decimal' in input_field:
        input_type = 'decimal'
        input_id = input_field['decimal']
        input_html = f'''
    <label for="{input_id}" class="form-label">{label}</label>
    <input type="number" step=".01" class="form-control" id="{input_id}">
'''
    elif 'select' in input_field:
        input_type = 'select'
        input_id = label.replace(' ', '_').lower()
        select_options_listname = f'select_{label.lower().replace(" ", "_")}_options'
        select_options_currentname = f'select_{label.lower().replace(" ", "_")}_current'
        input_html = f'''\n
    <label for="{input_id}" class="form-label">{label}</label>
    <select class="form-select mb-2" id="{input_id}" aria-label="Selecionar {label}">
        {{% for option_id, option_name in {select_options_listname} %}}
        <option {{{{'selected ' if option_id == {select_options_currentname} else ''}}}}value="{{{{option_id}}}}">{{{{option_name}}}}</option>
        {{% endfor %}}
    </select>
'''
    elif 'textarea' in input_field:
        input_type = 'textarea'
        if '{back.' in input_field['textarea']:
            input_content = input_field['textarea']
            input_id = label.replace(' ', '_').lower()
        else:
            input_id = input_field['textarea']
        input_html = f'''
    <div class="form-floating">
        <textarea class="form-control mb-2" id="{input_id}" style="height: 100px">{input_content}</textarea>
        <label for="{input_id}">{label}</label>
    </div>
'''
    elif 'table' in input_field:
        input_type = 'table'
        input_id = label.replace(' ', '_').lower()
        table_columns_listname = f'table_{label.lower().replace(" ", "_")}_columns'
        table_rows_listname = f'table_{label.lower().replace(" ", "_")}_rows'
        input_html = f'''\n
    <label for="{input_id}" class="form-label">{label}</label>
    <table id="{input_id}" class="table table-striped">
        <thead>
            <tr>
            {{% for column in {table_columns_listname} %}}
                <th>{{{{column}}}}</th>
            {{% endfor %}}
            <tr>
        </thead>
        <tbody>
            {{% for row in {table_rows_listname} %}}
                <tr>
                    {{% for value in row %}}
                        <td>{{{{value}}}}</td>
                    {{% endfor %}}
                </tr>
            {{% endfor %}}
        </tbody>
    </table>
'''
    return input_html, input_id, input_type, input_content


def generate_custom_template(route):
    route_title = route.get('title') or ''
    template_content = '''{% extends "layout.html" %}

    {% block inside_container %}\n'''
    template_content += f'<h1>{route_title}</h1>'
    if 'submit' in route:
        template_content += f'''<form action="" method="GET" id="form_{route_title.lower().replace(' ','_')}">\n'''
    if 'inputs' in route:
        for input_field in route['inputs']:
            input_html, _, _, _ = generate_input_html(input_field)
            template_content += input_html
    if 'submit' in route:
        template_content += f'''\n
<button class="btn btn-primary mb-2" type="submit">{route['submit']}</button>'''
        template_content += '\n</form>'
    template_content += '''\n{% endblock %}\n'''
    if 'backend' in route:
        template_content += f'''
{{% block scripts %}}
<script src="{{{{ url_for('static', filename='js/{route['endpoint'][1:].replace('/', '_')}.js') }}}}"></script>
{{% endblock %}}\n'''
    return template_content


def generate_custom_js(route):
    route_title = route.get('title') or ''
    js_content = ''
    if 'endpoint' in route['backend']:
        js_content = f'''
function load_resource() {{
    return $.ajax({{
        url: "{route['backend']['endpoint']}", 
        async: false,
        data: $('#form_{route_title.lower().replace(' ','_')}').serializeArray()
    }}).done(function(data) {{ return data; }});
}}\n
'''
    if 'outputs' in route:
        js_content += f'''
$('#form_{route_title.lower().replace(' ', '_')}').on('submit', function(e) {{
    e.preventDefault();'''
        for input_field in route['outputs']:
            input_html, input_id, input_type, input_content = generate_input_html(input_field)
            input_html = input_html.replace('id="', 'readonly id="')
            js_content += f'''
    $('.container').append(`{input_html}`);'''
            if input_type == 'textarea':
                output_content = input_content.replace('{back.', '${item.')
                js_content += f'''
    let item = load_resource().responseJSON;
    $('#{input_id}').val(`{output_content}`);'''
        js_content += f'''
}});'''
    return js_content
