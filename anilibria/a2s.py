from bs4 import BeautifulSoup
from shikimori import app, models

total = 0
missed = 0

def to_shiki_id(anime_name):
	global missed
	try:
		return app.db.session.query(models.AnimeVideo).filter(models.AnimeVideo.anime_english == anime_name).first().anime_id
	except:
		missed +=1
		#print(anime_name)
		#raise

def main():
	global total
	page = open("anilibria/releases.html", "rb").read().decode("u8")
	content_main = BeautifulSoup(page, features = "html5lib")
	releases = [td.find("a") for td in content_main.find_all("td", {'class': 'goodcell'})]
	releases_dict = dict()
	total = len(releases)
	for i, release in enumerate(releases):
		if (i % 100 == 0):
			print("[%d / %d] missed = %d" % (i, total, missed))
		alt_name = release.find("img").get("alt").split("/")[-1].strip()
		url = release.get("href")
		shiki_id = to_shiki_id(alt_name)
		if not shiki_id:
			continue
		releases_dict[shiki_id] = url
		#releases_dict[alt_name] = url
		#print(alt_name)
		#print(to_shiki_id(alt_name))
		#break

	open("shiki2anilibria.py", "wb").write(("shiki2anilibria = " + repr(releases_dict)).encode("u8"))
	print("total=%d\nmissed=%d" % (total, missed))

if __name__ == "__main__":
	main()
