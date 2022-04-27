import json

import feedparser
import feedgenerator
from jsonfeed import JSONFeed

from util import logger


class Cooker(object):
    def __init__(self, cfg):
        self.title = cfg["title"]
        self.description = cfg.get("description")
        self.home_page_url = cfg["home_page_url"]
        self.feed_url = cfg["feed_url"]

        self.feeds_urls = cfg["urls"]

    def cook(self):
        items = []

        for url in self.feeds_urls:
            logger.debug(f"Fetching {url}")
            try:
                i = self._fetch_items(url)
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
                continue

            logger.debug(f"Fetched {len(i)} items from {url}")
            items.extend(i)

        # TODO: sort by date
        # items.sort(key=lambda x: dateutil.parser.parse(x['date_published']), reverse=True)

        logger.debug(f"Final items {len(items)}")

        return {
            "title": self.title,
            "description": self.description,
            "home_page_url": self.home_page_url,
            "feed_url": self.feed_url,

            "items": items,
        }

    # fetch feed from url and mapping to json feed https://www.jsonfeed.org/version/1.1/
    @staticmethod
    def _fetch_items(url):
        feed = feedparser.parse(url)
        logger.info(f"Fetched {url}\n{feed}")
        # TODO: convert feed to json feed
        # TODO: use filter instead of hardcode limit
        return feed["entries"][:1]
