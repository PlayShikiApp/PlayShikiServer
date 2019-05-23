import os, sys

from shikimori import app
from sqlalchemy import func, distinct
from shikimori import models
from jinja2 import Environment, PackageLoader, select_autoescape
from shikimori import routes

ROOT_DIR = "."

episodes = app.db.session.query(distinct(models.AnimeVideo.anime_id), models.AnimeVideo.episode).all()

env = Environment(loader=PackageLoader('shikimori', 'templates'), autoescape=select_autoescape(['html', 'xml']))
template = env.get_template('video_template.html')

def render_template(anime_id, episode):
	anime_id = str(anime_id)
	episode = str(episode)
	out_path = os.path.join(ROOT_DIR, "static", "animes", anime_id, "%s.html" % episode)
	out_dir = os.path.dirname(out_path)
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)
	if not os.path.exists(out_path):
		routes.render_episode(anime_id, episode, out_file = out_path, template = template, static = "/static")

l = len(episodes)
def render_all(start, end):
	for n, (anime_id, episode) in enumerate(episodes[start:end]):
		print("%d of %d" % (n + 1, (end - start)))
		render_template(anime_id, episode)
render_all(int(sys.argv[1]), int(sys.argv[2]))
