import os, sys
from os.path import dirname, join, realpath
from collections import OrderedDict

SUBMODULES = [".."]

def _module_path():
	if "__file__" in globals():
		return THIS_PATH

	return ""

def setup_env():
	global SUBMODULES, THIS_PATH, TRANSLATIONS
	THIS_PATH = dirname(realpath(__file__))
	TRANSLATIONS = realpath(join(THIS_PATH, "../shikimori/pytranslations"))

	SUBMODULES = [join(THIS_PATH, sub) for sub in SUBMODULES]
	sys.path = SUBMODULES + sys.path

setup_env()
#print(sys.path)

from shikimori import models

def parse_model(self):
	elements = OrderedDict()
	for col in self.__table__.columns:
		if not (col.name.endswith("_from") or col.name.endswith("_up")):
			elements[col.name] = [col]
			continue

	range_name = col.name.replace("_from", "").replace("_up", "")
	if not range_name in elements:
		elements[range_name] = [col]
	else:
		elements[range_name].append(col)
	return elements

def gen_translations(model):
	#print(TRANSLATIONS)
	#print(parse_model(models.Student))
	res = ["from flask_babel import gettext", ""]
	for col in model.__table__.columns:
		k = col.name
		if k.endswith("_from"):
			k = k.replace("_from", "")
		elif k.endswith("_up"):
			continue
		res.append("gettext(\"%s\")" % k)

	out_filename = join(TRANSLATIONS, "%s.py" % model.__tablename__)
	with open(out_filename, "w") as f:
		f.write("\n".join(res))
