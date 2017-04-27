import os

import logging
import pprint

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATATBASE_URI = 'sqlite:///' + os.path.join(basedir, 'gutenberg.db')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATATBASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Squelch warnings
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MIME_UTF8 = 'text/plain'
MIME_ASCII = 'text/plain: charset=us-ascii'

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
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256))
    author_year_of_birth = db.Column(db.Integer)
    author_year_of_death = db.Column(db.Integer)
    downloads = db.Column(db.Integer)
    type = db.Column(db.String(64))  # 'Text'

    # Formats is a dict
    # We only need the text/plain key
    plaintext_url = db.Column(db.String(512))
    plaintext_filename = db.Column(db.String(256))

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
                 # language=None,
                 # subjects=None,
                 type=None     # Let's test for 'Text' before we create object and not store this
                 # LCC=None
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

        # Prefer to get UTF-8 version, fall back to ASCII if needed
        if MIME_UTF8 in formats:
            self.plaintext_url = formats[MIME_UTF8]
            self.plaintext_filename = self.plaintext_url.rsplit('/', 1)[-1]
        elif MIME_ASCII in formats:
            self.plaintext_url = formats[MIME_ASCII]
            self.plaintext_filename = self.plaintext_url.rsplit('/', 1)[-1]
        else:
            logger.warning("Can't find a plaintext version for ebook %d %s", self.ebook_id, self.title)
            logger.warning("Available formats:")
            logger.warning(pprint.pformat(formats))
            self.plaintext_url = None
            self.plaintext_filename = None
            # TODO throw error or something?

    def __repr__(self):
        return '{}: {} by {} ({}-{})'.format(
            self.ebook_id,
            self.title,
            self.author,
            self.author_year_of_birth,
            self.author_year_of_death
        )


