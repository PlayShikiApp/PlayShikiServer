from collections import OrderedDict
from parsers import playshikiapp, ongoings, anime365, sovetromantica, sibnet, anilibria, misc

df = playshikiapp.find_animes(parsers =
		      OrderedDict([
			("anilibria", anilibria.AnilibriaParser),
			("smotretanime", anime365.Anime365Parser),
			("sovetromantica", sovetromantica.SRParser),
			("sibnet", sibnet.SibnetParser)
		      ])
     )
playshikiapp.save(df, format = "sql")
