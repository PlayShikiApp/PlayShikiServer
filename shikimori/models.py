import pytz

from datetime import datetime
from collections import OrderedDict

from shikimori import app
from wtforms import Field, DecimalField, IntegerField, FloatField, SelectField, StringField, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField, DateField

from flask_babel import lazy_gettext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, BigInteger, Numeric, Float, String, DateTime, ForeignKey, Table
from sqlalchemy.types import Boolean, Date, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import generate_password_hash, check_password_hash
from wtforms.validators import Required, Length

app.db = SQLAlchemy(app)

class User(app.db.Model):
	__tablename__ = "users"
	id		= Column(Integer, primary_key = True)
	login		= Column(String(120), unique=True)
	pwdhash		= Column(String(300))
	role		= Column(String(120))

	def __init__(self, login, password, role, **kwargs):
		super(self.__class__, self).__init__(**kwargs)
		self.login = login.lower()
		self.set_password(password)
		self.set_role(role)

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def set_role(self, role):
		self.role = role

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

class Anime(app.db.Model):
	__tablename__ = "animes"
	id			= Column(Integer, primary_key = True)
	name			= Column(String(255))
	description_ru		= Column(Text)
	description_en		= Column(Text)
	kind			= Column(String(255))
	episodes		= Column(Integer, default = 0)
	duration		= Column(Integer)
	score			= Column(Numeric, default = 0)
	ranked			= Column(Integer)
	popularity		= Column(Integer)
	created_at		= Column(DateTime(timezone=False), default=datetime.now())
	updated_at		= Column(DateTime(timezone=False), default=datetime.now())
	image_file_name		= Column(String(255))
	image_content_type	= Column(String(255))
	image_file_size		= Column(Integer)
	image_updated_at	= Column(DateTime(timezone=False), default=datetime.now())
	aired_on		= Column(Date)
	released_on		= Column(Date)
	status			= Column(String(255))
	rating			= Column(String(255))
	episodes_aired		= Column(Integer)
	russian			= Column(String(255))
	censored		= Column(Boolean, default = False)
	imported_at		= Column(DateTime(timezone=False), default=datetime.now())
	next_episode_at		= Column(DateTime(timezone=False), default=datetime.now())
	tags			= Column(String(255))
	source			= Column(String(255))
	torrents_name		= Column(String(255))
	site_score		= Column(Numeric)
	desynced		= Column(Text, default = "{}")
	origin			= Column(Text)
	broadcast		= Column(Text)
	english			= Column(Text)
	japanese		= Column(Text)
	mal_id			= Column(Integer)
	authorized_imported_at	= Column(DateTime(timezone=False), default=datetime.now())
	synonyms		= Column(Text, default = "{}")
	cached_rates_count	= Column(Integer)
	genre_ids		= Column(Text, default = "{}")
	studio_ids		= Column(Text, default = "{}")
	season			= Column(Text)

class AnimeVideoAuthor(app.db.Model):
	__tablename__ = "anime_video_authors"
	id			= Column(Integer, primary_key = True)
	name			= Column(String(255))
	created_at		= Column(DateTime(timezone=False), default=datetime.now())
	updated_at		= Column(DateTime(timezone=False), default=datetime.now())
	is_verified		= Column(Boolean, default = False)

#id;url;anime_id;anime_english;anime_russian;episode;kind;language;quality;author;watches_count;uploader
class AnimeVideo(app.db.Model):
	__tablename__ = "anime_videos"
	id			= Column(Integer, primary_key = True)
	url			= Column(String(1000))
	anime_id		= Column(Integer)
	anime_english		= Column(Text)
	anime_russian		= Column(Text)
	episode			= Column(Integer)
	kind			= Column(String(255))
	quality			= Column(Text)
	language		= Column(String(255))
	author			= Column(String(255))
	watches_count		= Column(Integer)
	uploader		= Column(String(255))
	
	
app.db.create_all()
