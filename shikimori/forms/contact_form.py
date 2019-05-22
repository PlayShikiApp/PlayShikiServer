from flask_wtf import FlaskForm
from flask_babel import lazy_gettext, gettext, ngettext
from wtforms import Field, TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from .. import models

class ContactForm(FlaskForm):
	name = TextField(lazy_gettext("Name"),	[validators.Required(lazy_gettext("Please enter your name."))])
	email = TextField(lazy_gettext("Email"),	[validators.Required(lazy_gettext("Please enter your email address.")), \
						validators.Email(lazy_gettext("Please enter your email address."))])
	subject = TextField(lazy_gettext("Subject"),	[validators.Required(lazy_gettext("Please enter a subject."))])
	message = TextAreaField(lazy_gettext("Message"),	[validators.Required(lazy_gettext("Please enter a message."))])
	submit = SubmitField(lazy_gettext("Send"))
