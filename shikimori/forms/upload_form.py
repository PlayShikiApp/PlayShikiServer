from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_babel import gettext, ngettext
from wtforms import SubmitField, validators
from .. import models

class UploadForm(FlaskForm):
	file = FileField("Upload file", [validators.Required(gettext("Please choose file to upload"))])
	submit = SubmitField("Upload")
