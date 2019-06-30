from sqlalchemy import func

from shikimori import app, models
from parsers import ongoings

DEBUG = False
DRY_RUN = False

ongoings.main()
anime_ids = ongoings.ONGOING_IDS

all_videos = models.AnimeVideo.query.filter(models.AnimeVideo.anime_id.in_(anime_ids)).all()
res = dict()
dups = []
for v in all_videos:
	if v.url in res:
		dups.append(v.id)
		continue
	res[v.url] = v

print(dups)

if DEBUG:
	for id in dups:
		url = models.AnimeVideo.query.filter(models.AnimeVideo.id == id).first().url
		#print("%d: %d" % (id, app.db.session.query(func.count(models.AnimeVideo.url)).filter(models.AnimeVideo.url == url).scalar()) )
		others = [v.id for v in models.AnimeVideo.query.filter(models.AnimeVideo.url == url).all() if not v.id == id]
		print("%d: %s" % (id, str(others)))

if not DRY_RUN:
	models.AnimeVideo.query.filter(models.AnimeVideo.id.in_(dups)).delete(synchronize_session=False)
	app.db.session.commit()
