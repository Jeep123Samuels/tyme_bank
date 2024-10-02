import sqlite3

from flask import current_app, g
from flask_cors import CORS
from flask_migrate import Migrate
from flask_openapi3 import OpenAPI
from flask_sqlalchemy import SQLAlchemy


jwt = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT"
}
security_schemes = {"jwt": jwt}

app = OpenAPI(__name__, security_schemes=security_schemes)
CORS(app)
app.config.from_object('backend.config.BaseConfig')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


def connect_db():
    db_ = sqlite3.connect(
        current_app.config['SQLALCHEMY_DATABASE_URI'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_.row_factory = sqlite3.Row
    return db_


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def register_bps(app_):
    from backend.api.endpoints import GLOBAL_BLUEPRINTS

    for bp in GLOBAL_BLUEPRINTS:
        app.register_api(bp)
    return app_


app = register_bps(app)
if __name__ == "__main__":
    # with app.app ontext():
    #     db.create_all()
    app.run(debug=True)
