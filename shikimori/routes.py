#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import io
import random
import time
import base64

from functools import lru_cache
from collections import OrderedDict
from shikimori import app
from flask import Flask, render_template, render_template_string, request, jsonify, session, send_file, flash, url_for, redirect, abort
from flask_api import status
from flask_babel import gettext, ngettext, lazy_gettext
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_mail import Message, Mail
from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey, Table
from sqlalchemy import func

import urllib
import urllib.parse

import json
import demjson

from .models import User, Anime, AnimeVideo, AnimeVideoAuthor
from .forms import contact_form, upload_form, signup_form, signin_form
from werkzeug.utils import secure_filename

mail = Mail()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ""

@login_manager.user_loader
def load_user(user_id):
	return FlaskUser(user_id)

class FlaskUser(UserMixin):
	def __init__(self,id):
		self.id = id

@login_manager.unauthorized_handler
def unauthorized_callback():
	return redirect("/")

@app.route("/")
@app.basic_auth.required
def home():
	#session.clear()
	#return render_template("home.html")
	return redirect(url_for("play_episode", anime_id = 18689, episode = 1))

def allowed_file(filename):
	return os.path.splitext(filename)[1] in app.config["ALLOWED_EXTENSIONS"]

def ensure_folder_exists(folder):
	if not os.path.isdir(folder):
		os.makedirs(folder)

@app.route("/upload_file", methods=["GET", "POST"])
@login_required
def upload_file():
	form = upload_form.UploadForm()

	if request.method == "POST":
		if not form.validate_on_submit():
			return render_template("upload.html", form = form, success = False)

		# check if the post request has the file part
		if "file" not in request.files:
			return render_template("upload.html", form = form, no_selected_file = True)

		file = request.files["file"]
		# if user does not select file, browser also
		# submit an empty part without filename
		if file.filename == "":
			return render_template("upload.html", form = form, no_selected_file = True)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			user_folder = os.path.join(app.config["UPLOAD_FOLDER"], session["login"])
			ensure_folder_exists(user_folder)

			file.save(os.path.join(user_folder, filename))
			return render_template("upload.html", form = form, success = True)
		else:
			return render_template("upload.html", form = form, not_allowed_ext = True)

	return render_template("upload.html", form = form, success = False)

@app.route("/signup", methods=["GET", "POST"])
def signup():
	form = signup_form.SignupForm()

	if current_user.is_authenticated:
		return redirect(url_for("profile"))

	if request.method == "POST":
		if form.validate() == False:
			return render_template("signup.html", form = form)
		else:
			role = form.role.data

			new_user = User(form.login.data, form.password.data, role)
			app.db.session.commit()
			session["login"] = new_user.login
			login_user(FlaskUser(new_user.id))

			return redirect(url_for("profile"))
	elif request.method == "GET":
		return render_template("signup.html", form = form)

@app.route("/profile")
@login_required
def profile():
	user = User.query.filter_by(login = session["login"]).first()

	if user is None:
		return redirect(url_for("signin"))

	return render_template("profile.html")

@app.route("/about", methods=["GET", "POST"])
def about():
	return redirect("/")

@app.route("/contact", methods=["GET", "POST"])
def contact():
	return redirect("/")

@app.route("/signin", methods=["GET", "POST"])
def signin():
	if current_user.is_authenticated:
		redirect(url_for("profile"))

	form = signin_form.SigninForm()

	if request.method == "POST":
		if not form.validate():
			return render_template("signin.html", form = form)

		session["login"] = form.login.data
		user = User.query.filter_by(login = session["login"]).first()
		login_user(FlaskUser(user.id))
		if not user.student_id:
			return redirect(url_for("profile"))
		else:
			return redirect(url_for("student_form", id = [user.student_id]))

	elif request.method == "GET":
		return render_template("signin.html", form = form)



@app.route("/signout")
@login_required
def signout():
	logout_user()
	del session["login"]
	return redirect(url_for("home"))

def get_index(model):
	return app.db.session.query(func.max(model.id)).scalar()

@lru_cache(maxsize = None)
def get_anime_info(anime_id):
	res = OrderedDict()
	res["duration"] = app.db.session.query(func.max(AnimeVideo.episode)).filter_by(anime_id = anime_id).scalar()
	anime = AnimeVideo.query.filter_by(anime_id = anime_id).first()
	keys = ["anime_russian", "anime_english"]

	if not anime:
		abort(status.HTTP_404_NOT_FOUND)

	for key in keys:
		res[key] = getattr(anime, key)

	return res

def get_episodes_info(anime_id):
	res = OrderedDict()


from xor import bxor
KEY = open("key.priv", "rb").read()
key2 = open("key2.priv", "rb").read()

video_kinds = {"озвучка": "fandub", "оригинал": "raw", "субтитры": "subtitles"}

def handle_moved(anime_id):
	if anime_id.startswith("z"):
		return anime_id[1:]
	return anime_id

@app.route("/api_videos/<anime_id>", methods=["GET"])
@app.basic_auth.required
def anime_info(anime_id):
	return demjson.encode(get_anime_info(anime_id))

def serialize(obj):
	keys = obj.__table__.columns.keys()

	return OrderedDict([(attr, getattr(obj, attr)) for attr in keys])

def encode(s):
	return base64.b64encode(bxor(s.encode("u8"), key2))

@lru_cache(maxsize = None)
def get_max_episode_for_hosting(anime_id, video_hosting):
	video_hosting = "%" + video_hosting + "%"
	max_episode = app.db.session.query(func.max(AnimeVideo.episode)).filter(AnimeVideo.url.ilike(video_hosting)).filter_by(anime_id = anime_id).scalar()
	if not max_episode:
		return 0

	return max_episode

# sort videos by hostings
hostings_order = ["www.anilibria.tv", "online.animedia.tv", "sovetromantica.com", "vk.com", "video.sibnet.ru", "ok.ru", "mail.ru", "smotretanime.ru"]

def sort_videos_by_hostings(videos, order):
	res = []
	for hosting in order:
		host_videos = sorted([v for v in videos if urllib.parse.urlparse(v.url).netloc == hosting], key = lambda v: v.author)
		res += host_videos
		videos = [v for v in videos if urllib.parse.urlparse(v.url).netloc != hosting]
	res += videos
	return res

def get_videos_for_episode(anime_id, episode, video_id = None, decode_urls = "encode", sort_by_kinds = True, filter_by_kwargs = {}):
	anime_videos = sort_videos_by_hostings(AnimeVideo.query.filter_by(anime_id = anime_id, episode = episode).order_by(AnimeVideo.kind).all(), hostings_order)
	if sort_by_kinds:
		res = OrderedDict()
		for k in video_kinds.values():
			res[k] = []
	else:
		res = []

	if len(anime_videos) < 1:
		if sort_by_kinds:
			res["active_kind"] = "fansub"
			res["active_video"] = {"episode": 0}
		return res

	#print(video_id)
	try:
		video_id = int(video_id)
	except:
		video_id = None

	if not video_id in [a.id for a in anime_videos]:
		video_id = anime_videos[0].id

	keys = ["url", "video_hosting", "author", "uploader", "language", "id", "anime_id", "active", "episode"]
	if (not sort_by_kinds):
		keys.append("kind")

	active_video = None

	video_ids = []

	for n, v in enumerate(anime_videos):
		if decode_urls == "decode":
			v.url = bxor(v.url, KEY)
		elif decode_urls == "encode":
			v.url = base64.b64encode(bxor(v.url.encode("u8"), KEY)).decode("u8")

		v.video_hosting = urllib.parse.urlparse(v.url).netloc
		if (video_id is None) and n == 0:
			v.active = " active"
		else:
			v.active = " active" if (video_id == v.id) else ""

		#print("(%s == %s) is %d" % (video_id, v.id, video_id == v.id))

		if v.active:
			active_video = v

		if not v.language:
			v.language = "unknown"

		skip = False
		for key, val in filter_by_kwargs.items():
			if getattr(v, key) != val:
				skip = True
				break

		if skip:
			continue

		video_dict = {key: getattr(v, key) for key in keys}
		video_ids.append(v.id)
		
		if (sort_by_kinds):
			res[video_kinds[v.kind]].append(video_dict)
		else:
			res.append(video_dict)

	if (sort_by_kinds):
		res["ids"] = video_ids
	
		#print(res, active_video)
		if active_video is not None:
			res["active_kind"] = video_kinds[active_video.kind]
			res["active_video"] = serialize(active_video)
		else:
			res["active_kind"] = "fansub"
			res["active_video"] = {"episode": 0}

	return res

@app.route("/api/<anime_id>/<episode>", defaults={'video_id': None}, methods=["GET"])
@app.route("/api/animes/<anime_id>/<episode>", defaults={'video_id': None}, methods=["GET"])
@app.route("/api/<anime_id>/<episode>/<video_id>", methods=["GET"])
def api_videos(anime_id, episode, video_id):
	#return demjson.encode(get_videos_for_episode(anime_id, episode, video_id))
	return encode(json.dumps(get_videos_for_episode(handle_moved(anime_id), episode, video_id)))

@app.route("/<anime_id>", methods=["GET"])
@app.route("/animes/<anime_id>", methods=["GET"])
def api_anime_info(anime_id):
	return encode(json.dumps(get_anime_info(handle_moved(anime_id))))


@app.route("/faye", methods=["GET", "POST"])
def faye_stub():
	return "ok"

"""@app.route("/<anime_id>/<episode>", methods=["GET"])
def play_episode(anime_id, episode):
	html = render_episode(anime_id, episode, None, "")
	return base64.b64encode(bxor(html.encode("u8"), video_key))"""

def render_episode(anime_id, episode, video_id = None, static = "", out_file = "", template = ""):
	#session.clear()
	#return render_template("home.html")
	if not anime_id:
		abort(status.HTTP_404_NOT_FOUND)
	try:
		id = anime_id.split("-")[0]
		int(id)
	except:
		abort(status.HTTP_404_NOT_FOUND)
	anime_videos = get_videos_for_episode(anime_id, episode, video_id)
	anime_info = get_anime_info(anime_id)

	if out_file and template:
		ret = template.render(anime_id = anime_id, anime_videos = anime_videos, anime_info = anime_info, static = static)
		open(out_file, "w").write(ret)
		return
	return render_template("video_template.html", anime_id = anime_id, anime_videos = anime_videos, anime_info = anime_info, static = static)
