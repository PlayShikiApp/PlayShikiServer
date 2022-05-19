from collections import OrderedDict
from parsers import playshikiapp, ongoings, anime365, sovetromantica, sibnet, anilibria, nekomori, misc

df = playshikiapp.find_animes(parsers =
		      OrderedDict([
			("anilibria", anilibria.AnilibriaParser),
			#("nekomori", nekomori.NekoParser),
			#("smotretanime", anime365.Anime365Parser),
			#("sovetromantica", sovetromantica.SRParser),
			#("sibnet", sibnet.SibnetParser)
		      ]),
		      fetch_all_episodes = True, fetch_only_ongoings = False, anime_ids = [41109]
     )
playshikiapp.save(df, format = "sql")
