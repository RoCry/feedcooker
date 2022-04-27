import json

from feeds_config import feeds_cfg
from fetch import fetch_items

from util import logger


def cook_feed():
    items = []

    for url in feeds_cfg["urls"]:
        logger.debug(f"Fetching {url}")
        i = fetch_items(url)
        logger.debug(f"Fetched {len(i)} items from {url}")
        items.extend(i)

    # TODO: sort by date
    # items.sort(key=lambda x: dateutil.parser.parse(x['date_published']), reverse=True)

    logger.debug(f"Final items {len(items)}")

    return {
        "title": feeds_cfg["title"],
        "items": items,
    }


def main():
    feed = cook_feed()
    with open("./feeds.gen.json", "w") as f:
        f.write(json.dumps(feed, indent=2))


if __name__ == "__main__":
    main()
