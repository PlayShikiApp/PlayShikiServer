from jinja2 import Environment, PackageLoader, select_autoescape
from shikimori import routes

env = Environment(loader=PackageLoader('shikimori', 'templates'), autoescape=select_autoescape(['html', 'xml']))
template = env.get_template('video_template.html')
routes.render_episode("21", "2", out_file = "/home/chrono/one_piece-2.html", template = template)
