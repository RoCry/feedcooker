import datetime
import json

import feedparser
from jsonfeed import JSONFeed

from util import logger


class Cooker(object):
    def __init__(self, cfg):
        self.title = cfg["title"]
        self.description = cfg.get("description")
        self.home_page_url = cfg["home_page_url"]
        self.feed_url = cfg["feed_url"]

        self.feeds_urls = cfg["urls"]

    def cook(self) -> JSONFeed:
        feed = JSONFeed(
            title=self.title,
            link=self.home_page_url,
            description=self.description,
            feed_url=self.feed_url,
        )

        for url in self.feeds_urls:
            logger.debug(f"Fetching {url}")
            try:
                entries = self._fetch_entries(url)
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
                continue
            logger.debug(f"Fetched {len(entries)} entries from {url}\n{entries}")

            for e in entries:
                feed.add_item(**self._entry_to_feed_item(e))

        # TODO: sort by date
        # items.sort(key=lambda x: dateutil.parser.parse(x['date_published']), reverse=True)

        logger.debug(f"Final items {feed.num_items()}")

        return feed

    # fetch feed from url
    @staticmethod
    def _fetch_entries(url):
        feed = feedparser.parse(url)
        # TODO: use filter instead of hardcode limit
        return feed["entries"][:2]

    # mapping rss/atom entry to JSONFeed item(using in JSONFeed.add_item)
    @staticmethod
    def _entry_to_feed_item(e) -> dict:
        item = {
            "title": e["title"],
            "link": e["link"],
            "unique_id": e["id"],
        }

        summary = e.get("summary")
        content = e.get("content")
        if content and len(content) > 0:
            content = content[0].get("value")

        if content:
            # prefer use content as description
            item["description"] = content
            item["content"] = content
        elif summary:
            item["description"] = summary
        else:
            item["description"] = ""

        author_detail = e.get("author_detail")
        if author_detail:
            item["author_name"] = author_detail.get("name")
            item["author_email"] = author_detail.get("email")
            item["author_link"] = author_detail.get("href")
        elif e.get("author"):
            item["author_name"] = e.get("author")

        pubdate = e.get('published_parsed')
        if pubdate:
            item["pubdate"] = datetime.datetime(*pubdate[:6])

        updateddate = e.get('updated_parsed')
        if updateddate:
            item["updateddate"] = datetime.datetime(*updateddate[:6])

        logger.debug(f"item: {item}")
        return item
