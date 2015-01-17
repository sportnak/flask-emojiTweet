from app import db
from hashlib import md5

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(54))
	tweets = db.relationship('Tweets', backref='author', lazy='dynamic')
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	followed = db.relationship('User',
								secondary=followers,
								primaryjoin=(followers.c.follower_id == id),
								secondaryjoin=(followers.c.followed_id == id),
								backref=db.backref('followers', lazy = 'dynamic'),
								lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id) #python 2
		except NameError:
			return str(self.id) #python 3

	def avatar(self, size):
		return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

	@staticmethod
	def make_unique_nickname(nickname):
		if User.query.filter_by(nickname=nickname).first() is None:
			return nickname
		version = 2
		while True:
			new_nickname = nickname + str(version)
			if User.query.filter_by(nickname=new_nickname).first() is None:
				break
			else:
				version += 1
		return new_nickname

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_posts(self):
		return Tweets.query.join(followers, (followers.c.followed_id == Tweets.user_id)).filter(followers.c.follower_id == self.id).order_by(Tweets.timestamp.desc())

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Tweets(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	emoji = db.Column(db.Integer, db.ForeignKey('emojis.id'))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def location(self):
		if self.emoji:
			e = Emojis.query.all()[self.emoji - 1]
		else:
			e = Emojis.query.all()[0] #take one at random I guess
		if e and e.location:
			return e.location
		else:
			return 'http://www.gravatar.com/avatar/31bc83711bf83fff4d501aed7004523d?d=mm&s=50'

	def to_json(self):
		if self.user_id != 0:
			return {
				'id':self.id,
				'emoji': self.emoji,
				'timestamp': self.timestamp.strftime('%m/%d/%Y'),
				'user_id': self.user_id,
				'avatar': User.query.filter_by(id=self.user_id).first().avatar(128),
				'location': self.location()
			}
		return {
			'id':self.id,
			'emoji': self.emoji,
			'timestamp': self.timestamp.strftime('%m/%d/%Y'),
			'user_id': self.user_id,
			'avatar': 'http://www.gravatar.com/avatar/23d?d=mm&s=128',
			'location': self.location()
		}

	def __repr__(self):
		return '<Tweet %r>' % (self.emoji)

class Emojis(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String(100))
	counter = db.Column(db.Integer)

	def count(self, emoji):
		return Emojis.query.filter(emoji.location == Emojis.location).first().count

	def to_json(self):
		return {
			'id': self.id,
			'location': self.location,
			'counter': self.counter
		}

	def __repr__(self):
		return '<Emoji %r>' % (self.location)
