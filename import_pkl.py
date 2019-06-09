import sys

import pickle
from sqlalchemy import create_engine
from shikimori import routes, models

def import_to_db(filename = "shikimori.pkl"):
	engine = create_engine(open(".env").read(), echo=True, encoding="utf8")

	result = pickle.load(open(filename, "rb"))
	result.to_sql(name='anime_videos', con=engine, if_exists = 'append', index=False)

if __name__ == "__main__":
	import_to_db(sys.argv[1])
