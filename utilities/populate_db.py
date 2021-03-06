# import gc
import utilities.gutenberg_parse as g_parse
from gutencloud.db_orm import *

import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
PICKLE_FILE = os.path.join(BASEDIR, 'local_data', 'robot.pickle.gz')

# Note that the Flask imports and database setup is in db_orm.py


def main():
    create_destroy_db()
    fetch_parse_metadata()
    # link_dict = spider_urls()
    # match_urls(link_dict)


# Completely re-initialize the database
def create_destroy_db():
    db.drop_all()
    db.create_all()


def fetch_parse_metadata():

    # This will take a while
    logger.info('Fetching and parsing P.G. metadata. Please be patient...')
    metadata_catalog = g_parse.read_metadata()

    # We get back a list of dicts

    # Store that in the DB for now

    ebook_count = 0
    ebook_records = 0

    for _ebook in metadata_catalog:

        if _ebook['title'] is not None:  # Some entries appear to be dummies that break everything.
            if _ebook['type'] == 'Text':  # We only want text
                if _ebook['language'] is not None and 'en' in _ebook['language']:  # We only want English

                    # This constructs a new Ebook passing the dict as kwargs
                    # Python!
                    new_ebook = Ebook(**_ebook)

                    # Figure out the URI for the actual etext
                    # new_ebook.calculated_path = g_url.ebook_id_to_path(_ebook['id'])

                    db.session.add(new_ebook)
                    db.session.commit()
                    ebook_records += 1
                    # logger.debug('Added ebook %d to database', _ebook['id'])
                else:
                    # logger.debug('Ebook %d (%s) is not in English, not adding', _ebook['id'], _ebook['title'])
                    pass
            else:
                # logger.debug('Ebook %d (%s) is of type %s, not adding', _ebook['id'], _ebook['title'], _ebook['type'])
                pass
        else:
            # logger.debug('Ebook %d contains bogus data, skipping', _ebook['id'])
            pass

        ebook_count += 1
        if ebook_count % 1000 == 0:
            logger.info('Processed {} ebooks...'.format(ebook_count))

    logger.info('Metadata stored in database')
    logger.info('Created {} records. Continuing...'.format(ebook_records))

    # # Get that ginormous list out of memory before proceeding
    # del metadata_catalog
    # gc.collect()

if __name__ == "__main__":
    main()
