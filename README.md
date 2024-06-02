# DSL4UI
Gerador de aplicação web (flask) utilizando DSL.

# pacotes para rodar o gerador DSL4UI
```
conda install -y -c conda-forge pyyaml
```

# posicionar a especificação da aplicação Web no diretório private (arquivo dsl.yaml)

# executar o gerador para criar aplicação Web
```
python run_dsl4ui.py
```

# instalando ambiente e pacotes para rodar a aplicação gerada
```
conda create -y -n NOME_APLICACAO python=3.10.10
conda activate NOME_APLICACAO
pip install Flask SQLAlchemy Flask-SQLAlchemy flask-login werkzeug oauthlib
pip install mysqlclient #UTILIZE os pacotes para o SGBD desejado
conda install -y -c anaconda requests
```

# executar a aplicação Web gerada
```
set FLASK_APP=run
flask run
```
