from shikimori import app
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext, gettext, ngettext
from wtforms import PasswordField, Form, FormField, FieldList, SubmitField, IntegerField, StringField, TextAreaField, SelectField, SubmitField, validators, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .. import models

def municipality_choices():
	return models.Municipality.query

def default():
	return models.Municipality.query.filter(models.Municipality.id == '1').one_or_none()

class TestForm(FlaskForm):
	#name_of_municipality = StringField("name_of_municipality")
	name_of_municipality = SelectField(lazy_gettext('Role'), coerce = int)
	#name_of_municipality = SelectField(lazy_gettext('Role'), coerce = int)
	name_educational_organization = StringField("name_educational_organization")
	type_of_settlement = StringField("type_of_settlement")
	level_educational_organization = StringField("level_educational_organization")
	surname = StringField("surname")
	name = StringField("name")
	middle_name = StringField("middle_name")

	submit = SubmitField(lazy_gettext("Save"))

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)


class MemberForm(Form):
	name = StringField('name')
	member_id = StringField('member_id')
	inbox_share = IntegerField('inbox_share')
	# etc.

class TeamForm(Form):
	title = StringField('title')
	teammembers = FieldList(FormField(MemberForm))
