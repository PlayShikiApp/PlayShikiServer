from sqlalchemy import func

from shikimori import app, models
from parsers import ongoings, get_animes_ids, misc

DEBUG = False
DRY_RUN = False

#ongoings.main()
anime_ids = list(set(misc.MANUALLY_TRACKED_IDS + get_animes_ids.get_animes_ids("ongoings") + get_animes_ids.get_animes_ids("animes")))

def find_dups(anime_ids):
	all_videos = models.AnimeVideo.query.filter(models.AnimeVideo.anime_id.in_(anime_ids)).all()
	res = set()
	dups = set()
	for v in all_videos:
		if v.url in res:
			dups.add(v.id)
			continue
		res.add(v.url)

	print(dups)

	if DEBUG:
		for id in list(dups):
			url = models.AnimeVideo.query.filter(models.AnimeVideo.id == id).first().url
			#print("%d: %d" % (id, app.db.session.query(func.count(models.AnimeVideo.url)).filter(models.AnimeVideo.url == url).scalar()) )
			others = [(v.id, v.url) for v in models.AnimeVideo.query.filter(models.AnimeVideo.url == url).all() if not v.id == id]
			print("%d (%s): %s" % (id, url, str(others)))

	if not DRY_RUN:
		models.AnimeVideo.query.filter(models.AnimeVideo.id.in_(list(dups))).delete(synchronize_session=False)
		app.db.session.commit()


if __name__ == "__main__":
	total = len(anime_ids)
	buffer_len = 500
	#up_to = ((total // buffer_len) + (1 if (total % buffer_len) else 0)) * buffer_len
	up_to = (total // buffer_len + 1) * buffer_len
	for i in range(0, up_to, buffer_len):
		print("%d-%d" % (i, i + buffer_len))
		find_dups(anime_ids[i: i + buffer_len])
