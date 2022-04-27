import datetime

import feedparser
from jsonfeed import JSONFeed

from util import logger


class Cooker(object):
    def __init__(self, name: str, repository_owner: str, repository: str, recipe: dict):
        self.title = recipe["title"]
        self.description = recipe.get("description")
        self.home_page_url = f"https://github.com/{repository}"
        self.feed_url = f"https://github.com/{repository}/well-done/{name}.json"
        self.author_name = repository_owner
        self.author_link = f"https://github.com/{repository_owner}"

        self.feeds_urls = recipe["urls"]

    def cook(self) -> JSONFeed:
        feed = JSONFeed(
            title=self.title,
            link=self.home_page_url,
            description=self.description,
            feed_url=self.feed_url,
            author_name=self.author_name,
            author_link=self.author_link,
        )

        feed_items = []
        for url in self.feeds_urls:
            logger.debug(f"Fetching {url}")

            # TODO: support json feed
            try:
                f = self._parse_feed(url)
                # TODO: use filter instead of hardcode limit
                entries = f["entries"][:2]
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")
                continue
            logger.info(f"Fetched {len(entries)} entries from {url}\n{entries}")

            for e in entries:
                feed_items.append(self._entry_to_feed_item(f, e))

        feed_items.sort(key=lambda x: x['pubdate'], reverse=True)
        for i in feed_items:
            feed.add_item(**i)

        logger.debug(f"Final items {feed.num_items()}")

        return feed

    # fetch feed from url
    @staticmethod
    def _parse_feed(url):
        # TODO: improve fetch with ETAG/LAST-MODIFIED
        return feedparser.parse(url)

    # mapping rss/atom entry to JSONFeed item(using in JSONFeed.add_item)
    @staticmethod
    def _entry_to_feed_item(feed, e) -> dict:
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

        author_detail = (
            e.get("author_detail")
            if e.get("author_detail")
            else feed.get("author_detail")
        )
        if author_detail:
            item["author_name"] = author_detail.get("name")
            item["author_email"] = author_detail.get("email")
            item["author_link"] = author_detail.get("href")
        elif e.get("author"):
            item["author_name"] = e.get("author")
        elif feed.get("author"):
            item["author_name"] = feed.get("author")

        pubdate = e.get("published_parsed")
        if pubdate:
            item["pubdate"] = datetime.datetime(*pubdate[:6])
        else:
            item["pubdate"] = datetime.datetime.now()

        update = e.get("updated_parsed")
        if update:
            item["update"] = datetime.datetime(*update[:6])

        logger.debug(f"item: {item}")
        return item
