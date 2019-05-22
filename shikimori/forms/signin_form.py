from flask_wtf import FlaskForm
from flask_babel import lazy_gettext, gettext, ngettext
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from .. import models

class SigninForm(FlaskForm):
	login = TextField(lazy_gettext("Login"),	[validators.Required(lazy_gettext("Please enter your login.")), \
							validators.Required(lazy_gettext("Please enter your login."))])
	password = PasswordField(lazy_gettext('Password'), [validators.Required(lazy_gettext("Please enter a password."))])
	submit = SubmitField(lazy_gettext("Sign In"))

	def __init__(self, *args, **kwargs):
		FlaskForm.__init__(self, *args, **kwargs)

	def validate(self):
		if not FlaskForm.validate(self):
			return False

		user = models.User.query.filter_by(login = self.login.data).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.login.errors.append(lazy_gettext("Invalid login or password"))
			return False
