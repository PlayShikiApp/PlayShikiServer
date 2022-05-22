from collections import OrderedDict
from parsers import playshikiapp, ongoings, sovetromantica, sibnet, anilibria2, kodik, misc

from shiki_id import to_shiki_id

df = playshikiapp.find_animes(parsers =
		      OrderedDict([
			("anilibria2", anilibria2.AnilibriaParser2),
			#("sovetromantica", sovetromantica.SRParser),
			#("sibnet", sibnet.SibnetParser)
			#("kodik", kodik.KodikParser)
		      ]),
		      fetch_all_episodes = True, fetch_only_ongoings = False, anime_ids = [i for i in to_shiki_id]
     )
playshikiapp.save(df, format = "sql")
