from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField,SelectField, PasswordField, MultipleFileField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ContactForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    newspaper = BooleanField('Newspaper', default='checked')
    facebook = BooleanField('Facebook', default=False)
    submit = SubmitField("Submit")

class LoginForm(FlaskForm):    
    email = StringField("Email: ", validators=[Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])    
    submit = SubmitField("Login")

class SignupForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[Email()])
    usertype = SelectField(
        'User Type',
        choices=[('admin', 'Admin'), ('user', 'User')]
    )
    password = PasswordField("Password: ", validators=[DataRequired()])

    submit = SubmitField("Submit")

class UploadForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    upload = FileField('image', validators=[
        FileRequired('Haba'),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    files = MultipleFileField('File(s) Upload')
