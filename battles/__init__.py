import os

from flask import Flask

from flask.ext.sqlalchemy import SQLAlchemy


def create_app():
    config_obj = os.environ.get("CONFIG_MODULE", "config.test")
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db = SQLAlchemy(app)
    # app context, something or other ...
    # db.create_all()
    # db.init_app(app)

    # from battles.views.admin import admin
    # from battles.views.frontend import frontend
    # app.register_blueprint(admin)
    # app.register_blueprint(frontend)
    return app, db

app, db = create_app()

from battles.views import users, battles
app.register_blueprint(users)
app.register_blueprint(battles)
