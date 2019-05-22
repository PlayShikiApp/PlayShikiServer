pybabel extract -F shikimori/babel.cfg -k lazy_gettext -o shikimori/messages.pot shikimori
pybabel update -i shikimori/messages.pot -d shikimori/translations
