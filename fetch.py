import json

import feedparser
from util import logger


# fetch feed from url and mapping to json feed https://www.jsonfeed.org/version/1.1/
def fetch_items(url):
    feed = feedparser.parse(url)
    logger.info(f"Fetched {url}\n{feed}")
    # TODO: convert feed to json feed
    # TODO: use filter instead of hardcode limit
    return feed["entries"][:1]
