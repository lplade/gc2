import gc

import logging

from utilities import gutenberg
from utilities import url_harvester
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from gutencloud.orm import Ebook
from os import path

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    path.join('..', 'local_data', 'gutenberg.db')
db = SQLAlchemy(app)

# Completely re-initialize the database
db.drop_all()
db.create_all()

# This will take a while
metadata_catalog = gutenberg.read_metadata()

# We get back a list of dicts

# Store that in the DB for now

for _ebook in metadata_catalog:

    if _ebook['type'] == 'Text':
        # This constructs a new Ebook passing the dict as kwargs
        # Python!
        new_ebook = Ebook(**_ebook)

        db.session.add(new_ebook)
        db.session.commit()
        logger.debug('Added ebook %d to database', _ebook['id'])
    else:
        logger.debug('Ebook %d is of type %s, not adding', _ebook['id'], _ebook['type'])

# Get that ginormous list out of memory before proceeding
del metadata_catalog
gc.collect()

# This will also take a while
link_dict = url_harvester.spider()

for _link in link_dict:
