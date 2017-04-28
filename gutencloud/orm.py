import os

import logging
import pprint

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# sqlite is TOO SLOW for this
# basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# SQLALCHEMY_DATATBASE_URI = 'sqlite:///' + os.path.join(basedir, 'local_data', 'gutenberg.db')
# logger.info('Database at %s', SQLALCHEMY_DATATBASE_URI)

MYSQL_USER = os.environ['GC_MYSQL_USER']
MYSQL_PASSWORD = os.environ['GC_MYSQL_PASSWORD']

# Use utf8mb4 option to deal with a handful of i18n strings that show up
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@localhost/gutencloud?charset=utf8mb4'.format(MYSQL_USER, MYSQL_PASSWORD)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Squelch warnings
db = SQLAlchemy(app)

MIME_TXT = 'text/plain'
MIME_UTF8 = 'text/plain; charset=utf-8'
MIME_ISO = 'text/plain; charset=iso-8859-1'
MIME_ASCII = 'text/plain; charset=us-ascii'
MIME_ZIP = 'application/zip'


class Ebook(db.Model):
    """
The dict we pass into this looks like:
    {'LCC': {'PS'},
 'author': u'Burroughs, Edgar Rice',
 'authoryearofbirth': 1875,
 'authoryearofdeath': 1950,
 'downloads': 401,
 'formats': {'application/epub+zip': 'http://www.gutenberg.org/ebooks/123.epub.noimages',
  'application/prs.plucker': 'http://www.gutenberg.org/ebooks/123.plucker',
  'application/x-mobipocket-ebook': 'http://www.gutenberg.org/ebooks/123.kindle.noimages',
  'application/x-qioo-ebook': 'http://www.gutenberg.org/ebooks/123.qioo',
  'text/html; charset=iso-8859-1': 'http://www.gutenberg.org/files/123/123-h.zip',
  'text/plain': 'http://www.gutenberg.org/ebooks/123.txt.utf-8',
  'text/plain; charset=us-ascii': 'http://www.gutenberg.org/files/123/123.zip'},
 'id': 123,
 'language': ['en'],
 'subjects': {'Adventure stories',
  'Earth (Planet) -- Core -- Fiction',
  'Fantasy fiction',
  'Science fiction'},
 'title': u"At the Earth's Core",
 'type': 'Text'}
    """

    # TODO Really, author, formats, languages, and subjects
    # should be their own tables/objects

    ebook_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    # 191 characters is limit for InnoDB using utf8mb4
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.Text)
    author_year_of_birth = db.Column(db.Integer)
    author_year_of_death = db.Column(db.Integer)
    downloads = db.Column(db.Integer)
    # type = db.Column(db.String(64))  # 'Text'
    # Formats is a dict
    # language is a list of ISO codes
    # We are already filtering for 'en'
    # languages = db.Column(db.PickleType)

    # subjects is a set of strings?
    # We aren't using this
    # subjects = db.Column(db.PickleType)

    # lcc is a list of two-letter codes (set?)
    # We aren't using this either
    # lcc = db.Column(db.PickleType)

    def __init__(self, id, title, *,
                 # First two are required to construct
                 # Rest can be passed as kwargs from dict
                 author=None,
                 authoryearofbirth=None,
                 authoryearofdeath=None,
                 downloads=None, formats=None,
                 language=None,
                 subjects=None,
                 type=None,     # Let's test for 'Text' before we create object and not store this
                 LCC=None
                 ):
        self.ebook_id = id
        self.title = title
        self.author = author
        self.author_year_of_birth = authoryearofbirth
        self.author_year_of_death = authoryearofdeath
        self.downloads = downloads
        # self.languages = language
        # self.subjects = subjects
        # self.type = type
        assert type == 'Text'
        # self.lcc = LCC

    def __repr__(self):
        if self.author is not None:
            if self.author_year_of_birth is not None:
                repr_string = '{}: {} by {} ({}-{})'.format(
                    self.ebook_id,
                    self.title,
                    self.author,
                    self.author_year_of_birth,
                    self.author_year_of_death  # We're fine if this is None
                )
            else:
                repr_string = '{}: {} by {}'.format(
                    self.ebook_id,
                    self.title,
                    self.author
                )
        else:
            repr_string = '{}: {}'.format(
                self.ebook_id,
                self.title
            )
        return repr_string


