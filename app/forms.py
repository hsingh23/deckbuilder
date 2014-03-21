from flask.ext.wtf import Form
# from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import Required

class KeywordForm(Form):
    keywords= StringField('keywords', validators = [Required()])
