# Based on
# https://github.com/c-w/Gutenberg/blob/master/gutenberg/acquire/text.py

import os
from time import sleep

import requests
from gutencloud.orm import *
from werkzeug.contrib.cache import FileSystemCache
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Change this if something breaks or you are banned
GUTENBERG_MIRROR = 'http://aleph.gutenberg.org'

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, 'local_data', 'cache')
# Set up werkzeug cache
cache = FileSystemCache(CACHE_DIR)


def ebook_id_to_path(ebook_id):
    """
    Returns the subdirectory that an etextno will be found in a gutenberg 
    mirror. Generally, one finds the subdirectory by separating out each digit 
    of the etext number, and uses it for a directory. The exception here is for 
    etext numbers less than 10, which are prepended with a 0 for the directory 
    traversal.
    :param ebook_id: int
    :return: str
    """
    id_string = str(ebook_id).zfill(2)
    all_but_last_digit = list(id_string[:-1])
    subdir_part = '/'.join(all_but_last_digit)
    subdir = '{0}/{1}'.format(subdir_part, ebook_id)  # id_string not zfilled
    return subdir


def check_mirror_exists(mirror):
    response = requests.head(mirror)
    if not response.ok:
        error = 'Could not reach Gutenberg mirror "{0:s}". ' \
                'Try setting a different mirror ' \
                '(https://www.gutenberg.org/MIRRORS.ALL)'
        logger.error(error)
        return False
    else:
        return True


def format_download_uri(ebook_id, mirror=None):
    """
    Returns the download location on the Project Gutenberg servers for a given text.
    :param ebook_id: PG ebook id number
    :param mirror: Site to download from
    :return: Full URI to download, or None if error
    """
    uri_root = mirror or GUTENBERG_MIRROR
    uri_root = uri_root.strip().rstrip('/')
    # check_mirror_exists(uri_root)   # ONLY DO THIS ONCE!

    extensions = ('.txt', '-8.txt', '-0.txt')
    for extension in extensions:
        path = ebook_id_to_path(ebook_id)
        uri = '{root}/{path}/{ebook_id}{extension}'.format(
            root=uri_root,
            path=path,
            ebook_id=ebook_id,
            extension=extension
        )
        sleep(2)
        response = requests.head(uri)
        if response.ok:
            return uri

    logger.warning('Failed to find {0} on {1}.'.format(ebook_id, uri_root))
    return None


def load_etext(ebook_id, refresh_cache=False, mirror=None):

    # TODO validate ebook_id

    mirror = mirror or GUTENBERG_MIRROR

    # Set unique key value for caching
    text_key = os.path.join(CACHE_DIR, '{}.txt'.format(ebook_id))

    # Purge key if requested
    if refresh_cache:
        cache.delete(text_key)
        # TODO does this fail elegantly if key doesn't already exist?

    # Attempt to retrieve the etext from the cache
    etext = cache.get(text_key)
    if etext is None:
        # go get it
        download_uri = format_download_uri(ebook_id, mirror)
        if download_uri:
            sleep(2)
            response = requests.get(download_uri)
            etext = response.text
            # cache texts for a week
            cache.set(text_key, etext, timeout=60*60*24*7)
        # else leave etext set to None
    else:
        logger.debug('Found etext {} in cache, using it'.format(text_key))

    return etext

