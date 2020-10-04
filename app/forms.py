from flask_wtf import FlaskForm
from wtforms import  StringField, SubmitField

class GetShortenUrl(FlaskForm):
    url = StringField('Enter Your URL !!')
    submit = SubmitField('Submit')

class GetOriginUrl(FlaskForm):
    url = StringField('Enter Your Shorten URL !!')
    submit = SubmitField('Submit')

class Search(FlaskForm):
    search = StringField('Enter Your URL !!')
    submit = SubmitField('Submit') 