import json
import os
from flask import send_from_directory, make_response, render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EditForm, RegisterForm, ChangePasswordForm, UploadForm
from .models import User, Tweets, Emojis
from datetime import datetime
from config import POSTS_PER_PAGE, UPLOADS_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename, generate_password_hash, check_password_hash

@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated():
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit() and 'register' not in request.form:
		session['remember_me'] = form.remember_me.data
		if form.validate():
			remember_me = False
			user = User.query.filter_by(email=form.email.data).first()
			if 'remember_me' in session:
				remember_me = session['remember_me']
				session.pop('remember_me', None)
			login_user(user, remember = remember_me)
			return redirect(request.args.get('next') or url_for('index'))
		return redirect(url_for('index'))
	if 'register' in request.form:
		return redirect(url_for('register'))
	return render_template('login.html',
							title='Sign In',
							form = form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/post/<int:id>', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1, id = -1):
	if id > 0:
		if g.user is not None and g.user.is_authenticated():
			tweets = Tweets(emoji=id, timestamp=datetime.utcnow(), user_id = g.user.id)
		else:
			tweets = Tweets(emoji=id, timestamp=datetime.utcnow(), user_id = 0)
		db.session.add(tweets)
		db.session.commit()
		flash('Your post is now live!')
		return redirect(url_for('index'))
	elif g.user is not None and g.user.is_authenticated():
		user = g.user
		tweets = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)

		return render_template('index.html',
								title='Home',
								user=user,
								tweets=tweets)
	else:
		tweets = Tweets.query.paginate(page, POSTS_PER_PAGE, False)
		return render_template('index.html',
							title='Home',
							user= None,
							tweets = tweets)

@app.route('/tweets')
@app.route('/tweets/<int:user>')
def tweets(user=0):
	if user <= 0:
		posts = Tweets.query.order_by(Tweets.timestamp.desc())
	else: # user 
		posts = Tweets.query.filter('user_id=='+str(user)).order_by(Tweets.timestamp.desc())

	tweets = []
	if posts is not None:
		tweets = [post.to_json() for post in posts]
		response = make_response()
		response.data = json.dumps(tweets)
	return response

@app.route('/emojis')
def emojis():
	posts = Emojis.query.order_by(Emojis.id.asc())

	emojis = []
	if posts is not None:
		emojis = [post.to_json() for post in posts]
		response = make_response()
		response.data = json.dumps(emojis)
	return response
# EUREKA - [array] = [before tweets] + [shown tweets] + [after tweets]

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
	user = User.query.filter_by(nickname=nickname).first()
	if user == None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	posts = user.tweets.paginate(page, POSTS_PER_PAGE, False)
	return render_template('user.html',
							user = user,
							posts = posts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
	form = EditForm(original_nickname =g.user.nickname)
	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('edit'))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me
	return render_template('edit.html', form=form)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user is None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t follow yourself!')
		return redirect(url_for('user', nickname=nickname))
	u = g.user.follow(user)
	if u is None:
		flash('Cannot follow ' + nickname + '.')
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('You are now following ' + nickname + '!')
	return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
	user = User.query.filter_by(nickname=nickname).first()
	if user is None:
		flash('User %s not found.' % nickname)
		return redirect(url_for('index'))
	if user == g.user:
		flash('You can\'t unfollow yourself!')
		return redirect(url_for('user', nickname=nickname))
	u = g.user.unfollow(user)
	if u is None:
		flash('Cannot unfollow ' + nickname + '.')
		return redirect(url_for('user', nickname=nickname))
	db.session.add(u)
	db.session.commit()
	flash('You have stopped following ' + nickname + '.')
	return redirect(url_for('user', nickname=nickname))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if g.user is not None and g.user.is_authenticated():
		return redirect(url_for('index'))

	form = RegisterForm()
	if form.validate_on_submit():
		if form.validate():
			g.user.nickname = form.username.data
			g.user.email = form.email.data
			g.user.password = generate_password_hash(form.password.data)
			u = User(nickname = form.username.data, email = form.email.data, password = g.user.password)
			db.session.add(u)
			db.session.commit()

			flash('You have been registered!')
			return redirect(request.args.get('next') or url_for('index'))
		return redirect(url_for('index'))
	return render_template('register.html',
							title='Register',
							form = form)

@app.route('/password', methods=['GET', 'POST'])
def password():
	if g.user is None:
		return redirect(url_for('index'))
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if form.validate():
			password = generate_password_hash(form.new_password.data)
			u = User.query.filter_by(email=form.email.data).first()
			u.password = password
			db.session.commit()

			flash('Your password has been changed to *******!')
			flash('Just kidding, we wouldnt be silly enough to show you your password')
			return redirect(request.args.get('next') or url_for('index'))
	return render_template('change_password.html',
							title='Change Password',
							form = form)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
	form = UploadForm()
	if form.validate_on_submit():
		file = form.filename.data
		if file:
			filename = secure_filename(file.filename)
			location = os.path.join(UPLOADS_FOLDER, filename)
			u = User.query.filter_by(id = g.user.id).first()
			if u.location is not None:
				os.remove(os.path.join(UPLOADS_FOLDER, u.location))
			u.location = filename
			db.session.commit()
			file.save(location)
			return redirect(url_for('index', filename=filename))
	return render_template('upload.html',
							filename=None,
							form = form)

@app.route('/uploaded/<filename>')
@login_required
def uploaded(filename):
	return send_from_directory(UPLOADS_FOLDER, filename)


@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

# basic functions

def allowed_file(filename):
	filetype= filename.split('.')[1]
	return filetype in ALLOWED_EXTENSIONS
