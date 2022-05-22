from collections import OrderedDict
from parsers import playshikiapp, ongoings, anime365, sovetromantica2, sibnet, anilibria2, nekomori, misc

from shiki2sovetromantica import shiki2sovetromantica
df = playshikiapp.find_animes(parsers =
		      OrderedDict([
			#("anilibria2", anilibria2.AnilibriaParser2),
			#("nekomori", nekomori.NekoParser),
			#("smotretanime", anime365.Anime365Parser),
			("sovetromantica2", sovetromantica2.SRParser2),
			#("sibnet", sibnet.SibnetParser)
		      ]),
		      fetch_all_episodes = True, fetch_only_ongoings = False, anime_ids = [i for i in shiki2sovetromantica][30:40]
		      #fetch_all_episodes = True, fetch_only_ongoings = False, anime_ids = [33489]
     )
playshikiapp.save(df, format = "sql")
