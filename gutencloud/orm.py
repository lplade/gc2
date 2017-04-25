import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATATBASE_URI = 'sqlite:///' + os.path.join(basedir, 'gutenberg.db')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATATBASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Squelch warnings
db = SQLAlchemy(app)


class Ebook(db.Model):
    '''
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
    '''

    # TODO Really, author, formats, languages, and subjects
    # should be their own tables/objects

    ebook_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    author = db.Column(db.String(256))
    author_year_of_birth = db.Column(db.Integer)
    author_year_of_death = db.Column(db.Integer)
    downloads = db.Column(db.Integer)
    type = db.Column(db.String(64))  # 'Text'
    # Formats is a dict
    formats = db.Column(db.PickleType)
    # language is a list of ISO codes
    languages = db.Column(db.PickleType)
    # subjects is a dict
    subjects = db.Column(db.PickleType)

    def __init__(self, ebook_id, title, **kwargs):
        self.ebook_id = ebook_id
        self.title = title
        # TODO parse kwargs

    def __repr__(self):
        return '{}: {} by {} ({}-{})'.format(
            self.ebook_id,
            self.title,
            self.author,
            self.author_year_of_birth,
            self.author_year_of_death
        )
