import os

import pandas as pd

from collections import OrderedDict
from bs4 import BeautifulSoup
from pprint import pprint
#from percache import Cache

url_to_id = lambda url: int("".join([i for i in url.split("/")[-1].split("-")[0] if i.isdigit()]))

def parse_article(article):
	a = article.find("a")
	anime_id = url_to_id(a.get("href"))
	try:
		anime_english = article.find("span", {"class": "name-en"}).text
	except:
		anime_english = ""
	if not anime_english:
		try:
			anime_english = a.text
		except:
			pass
	try:
		anime_russian = article.find("span", {"class": "name-ru"}).get("data-text")
	except:
		anime_russian = ""
	return anime_id, anime_english, anime_russian

def parse_articles():
	res = pd.DataFrame(columns = ["anime_id", "anime_english", "anime_russian"])
	#c = 0
	for i in os.listdir("animes1"):
		print(i)
		if not i.endswith(".html"):
			continue
		h1 = BeautifulSoup(open("animes1/%s" % i).read(), features="html5lib")
		articles = h1.find_all("article")

		tmp_res = pd.DataFrame(columns = ["anime_id", "anime_english", "anime_russian"])
		for a in articles:
			anime_id, anime_english, anime_russian = parse_article(a)
			tmp_res = tmp_res.append({
                "anime_id": anime_id,
                "anime_english": anime_english,
                "anime_russian": anime_russian.encode("u8"),
            }, ignore_index = True)

		res = res.append(tmp_res, ignore_index = True, sort = False)
		#if c == 2: break
		#c += 1

	return res

df = parse_articles()
df.to_json('shiki_db.json', orient='records', lines=True, force_ascii=False)