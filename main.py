from dynaconf import FlaskDynaconf
from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from routes.user import user
from routes.chat import chat
import os

app = Flask(__name__)
FlaskDynaconf(app, settings_files=["settings.toml"])

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{app.config['POSTGRES_USER']}:"
    f"{app.config['POSTGRES_PASSWORD']}@"
    f"{app.config['POSTGRES_HOST']}:"
    f"{app.config['POSTGRES_PORT']}/"
    f"{app.config['POSTGRES_DB_NAME']}"
)

db = SQLAlchemy(app)

app.register_blueprint(user)
app.register_blueprint(chat)
embedding = None

@app.errorhandler(Exception)
def exceptions(e):
    return jsonify({
        'error': 'Internal Server Error',
        'error_message': str(e)
    }), 500

@app.route("/")
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(
        host=app.config.get("HOST"),
        port=app.config.get("PORT"),
        debug=app.config.get("DEBUG"),
    )
