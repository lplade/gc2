"""
Project Gutenberg does not offer a straightforward means to directly
download etexts with automation. There's a big list of index pages intended
to be spidered with wget.

We read through all these pages, parse the URLs and associate them with ebook id numbers.
The URLs can later be associated with ebook metadata.

Respect these wget options:

wget -w 2 -m -H "http://www.gutenberg.org/robot/harvest?filetypes[]=txt&langs[]=en"

-w 2  Wait 2 seconds between retrievals
-m    Mirroring options: -r -N -l inf --no-remove-listing
-H    Span hosts

-r    Recursive
-N    Time-stamping
-l inf Infinite recursion depth


"""

import time
import logging
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

BASE_URL = 'http://www.gutenberg.org/robot/harvest'
BASE_PARAMS = {
    'filetypes': 'txt',
    'langs': 'en'
    # The other param possible is 'offset'
}


class GBHarvestPage:
    """
    Lets us pass data derived from a harvest page request
    """
    offset = 0
    link_list = []  # GBHarvestLinks
    new_offset = None

    def __init__(self, offset, link_list, new_offset):
        self.offset = offset
        self.link_list = link_list
        self.new_offset = new_offset


class GBHarvestLink:
    """
    Lets us pass data derived from a harvest page link
    """
    filename = ''
    url = ''

    def __init__(self, filename, url):
        self.url = url
        self.filename = filename


def spider():
    offset = 0
    link_dict = {}  # {filename: url}
    while True:

        # New page
        new_offset = None

        # Get the next page of links
        try:
            r = get_request(offset=offset)

            c = r.content

            # TODO modularize this

            soup = BeautifulSoup(c, 'html.parser')
            for link in soup.find_all('a'):
                if link.string == 'Next Page':

                    # Extract the offset from the 'Next Page' link
                    next_page_url = link.get('href')
                    o = urlparse(next_page_url)
                    new_offset = o.params('offset')  # TODO error check

                else:
                    ebook_url = link.get('href')

                    # Split URL string on '/' and get the rightmost
                    ebook_filename = ebook_url.rsplit('/', 1)[-1]

                    # Add dict entry based on those items
                    link_dict.update(dict([ebook_filename, ebook_url]))

        except ConnectionError:
            # TODO more graceful error handling
            logger.error('Returned HTTP %s, aborting', r.status_code)
            r.raise_for_status()
            exit()

        # Having parsed all the links in the page now...
        if new_offset is not None:
            offset = new_offset
            logger.debug('Continuing to next page at offset %d', offset)
            continue
        else:
            logger.debug("Can't find more pages to parse")
            break  # out of initial while loop

    # At this point we should have run out of pages to parse
    # So we do stuff with the collected data
    logger.debug('Collected %d links', len(link_dict))
    return link_dict


def get_request(offset=0, delay=2):
    wait(delay)  # Wait 2 seconds before starting or get banned
    payload = BASE_PARAMS
    if offset != 0:
        # If an offset was specified, include it as a param
        payload.update({'offset': str(offset)})
    # Return the whole request object so we can check its status
    return requests.get(BASE_URL, params=payload)


def wait(seconds):
    logger.debug('Waiting %d seconds...', seconds)
    time.sleep(seconds)
    return True


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
