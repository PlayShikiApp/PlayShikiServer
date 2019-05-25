#!/usr/bin/env python3

import sys

from shikimori import app
from shikimori import models
import xor

def usage():
	print("usage: encode_db_urls.py <key>")
	sys.exit()

if len(sys.argv) != 2:
	usage()

KEY = open(sys.argv[1], "rb").read()

videos = models.AnimeVideo.query.all()
for v in videos:
	v.url = xor.bxor(v.url.encode("u8"), KEY)

app.db.session.commit()
