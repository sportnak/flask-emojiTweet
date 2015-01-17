from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from werkzeug import generate_password_hash, check_password_hash
from .models import User, Tweets

class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(email=self.email.data).first()
		if user == None:
			self.email.errors.append('Incorrect email or password')
			return False
		if check_password_hash(user.password, self.password.data):
			return True
		self.email.errors.append('Incorrect email or password')
		return False

class RegisterForm(Form):
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[
		DataRequired(),
		EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('Confirm Password')
	username = StringField('Username', validators=[DataRequired()])

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(nickname=self.username.data).first()
		if user != None:
			self.username.errors.append('This nickname is already in user. Please choose another one')
			return False
		return True	


class EditForm(Form):
	nickname = StringField('nickname', validators=[DataRequired()])
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])	

	def __init__(self, original_nickname, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.original_nickname = original_nickname

	def validate(self):
		if not Form.validate(self):
			return False
		if self.nickname.data == self.original_nickname:
			return True
		user = User.query.filter_by(nickname=self.nickname.data).first()
		if user!= None:
			self.nickname.errors.append('This nickname is already in use. Please choose another one.')
			return False
		return True
