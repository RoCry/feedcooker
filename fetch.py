import feedparser


# fetch feed from url and mapping to json feed https://www.jsonfeed.org/version/1.1/
def fetch_items(url):
    feed = feedparser.parse(url)
    # TODO: convert feed to json feed
    return feed["entries"]
