from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokeDex(FlaskForm):
    pokereq = StringField('pokereq')
    submit = SubmitField()