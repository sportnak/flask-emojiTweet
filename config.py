import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'app.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

UPLOADS_FOLDER = os.path.realpath('.') + '\\uploads'
ALLOWED_EXTENSIONS = set(['xt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

FILE_SYSTEM_STORAGE_VIEW = 'uploads'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'sportnak@gmail.com'
MAIL_PASSWORD = '00michael'

#administrator list
ADMINS = ['sportnak@gmail.com']

#pagination
POSTS_PER_PAGE = 3