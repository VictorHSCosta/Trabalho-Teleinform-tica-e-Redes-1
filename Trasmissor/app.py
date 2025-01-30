from flask import Flask
from routes import app as app_routes

app = app_routes  # Importa as rotas do arquivo routes.py

if __name__ == "__main__":
    app.run(debug=True)  # Ativa o modo debug para facilitar o desenvolvimento
