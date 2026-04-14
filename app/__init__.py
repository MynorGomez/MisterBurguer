from flask import Flask
from flask_mysqldb import MySQL

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mysql.init_app(app)

    from app.routes.auth import auth
    from app.routes.public import public
    from app.routes.cocina import cocina
    from app.routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(public)
    app.register_blueprint(cocina)
    app.register_blueprint(admin)

    return app