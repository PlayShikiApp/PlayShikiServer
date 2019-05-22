from os.path import join, realpath, dirname
from flask import g, request
from flask import Flask
from flask_babel import Babel
from flask_session import Session
from flask_jsglue import JSGlue

from datetime import timedelta

root_dir = realpath(join(dirname(__file__), ".."))
dot_env = realpath(join(root_dir, "../.env"))

flask_templates_dir = realpath(join(dirname(__file__), "templates"))
app = Flask(__name__, template_folder = flask_templates_dir)
app.config["TEMPLATES_DIR"] = flask_templates_dir

app.config["DATAFRAMES_DIR"] = realpath(join(dirname(__file__), "dataframes"))

UPLOAD_FOLDER = join(root_dir, "uploads")
ALLOWED_EXTENSIONS = set([".docx", ".xlsx", ".txt", ".pdf", ".png", ".jpg", ".jpeg", ".gif"])

app.secret_key = "development key"

app.session = Session()
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
# The maximum number of items the session stores
# before it starts deleting some, default 500
app.config['SESSION_FILE_THRESHOLD'] = 100
app.session.init_app(app)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["CACHE_TYPE"] = "null"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "contact@example.com"
app.config["MAIL_PASSWORD"] = "your-password"
app.config["SQLALCHEMY_DATABASE_URI"] = open(dot_env, "r").read().split("\n")[0]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

from .routes import mail
mail.init_app(app)

import shikimori.models
app.db.init_app(app)

import shikimori.routes

app.babel = Babel(app)

@app.babel.localeselector
def get_locale():
	# if a user is logged in, use the locale from the user settings
	#ser = getattr(g, "user", None)
	#if user is not None:
	#	return user.locale
	# otherwise try to guess the language from the user accept
	# header the browser transmits.  We support ru/en in this
	# example.  The best match wins.
	return request.accept_languages.best_match(["ru"])

app.jsglue = JSGlue(app)
