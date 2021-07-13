from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo



class LoginForm(FlaskForm):
    email    = StringField("E-mail", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit   = SubmitField("Verstuur")
    
    
class RegistrationForm(FlaskForm):
    email     = StringField("E-mail", validators=[DataRequired()])
    password  = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField("Register")