import gc
from utilities import gutenberg
from utilities import url_harvester
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gutencloud.orm import Ebook
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    path.join('..', 'local_data', 'gutenberg.db')
db = SQLAlchemy(app)

db.create_all()


# This will take a while
md = gutenberg.read_metadata()

# We get back a list of JSON elements

# Store that in the DB for now

for _ebook in md:
    # This constructs a new Ebook passing the dict as kwargs
    # Python!
    new_ebook = Ebook(**_ebook)


# Get that ginormous list out of memory before proceeding
del md
gc.collect()

