def generate_layout_template(dsl_app):
    app_title = dsl_app['title'] if 'title' in dsl_app else 'Default'
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
    layout_content += f'''<a class="nav-link active" href="{{{{ url_for('home') }}}}">{app_title}</a>'''
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
    app_title = dsl_app['title'] if 'title' in dsl_app else 'Default'
    home_content = '''{% extends "layout.html" %}

{% block inside_container %}\n'''
    home_content += f'<h1>{app_title}</h1>\n'
    home_content += '''{% endblock %}
'''
    return home_content
