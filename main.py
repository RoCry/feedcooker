from feedgenerator import SyndicationFeed

from recipes import get_recipes
from cooker import Cooker
import fire

from util import url_to_valid_filename, put_github_action_env, xml_escape

all_feed_files = set()


def main(repository: str, repository_owner: str, limit=20):
    recipes = get_recipes()

    json_feeds = []
    atom_feeds = []
    for name in recipes:
        normalized_name = url_to_valid_filename(name)
        cooker = Cooker(
            name=name,
            normalized_name=normalized_name,
            repository=repository,
            repository_owner=repository_owner,
            recipe=recipes[name],
            limit=recipes[name].get("limit", limit),
        )
        json_feed, atom_feed = cooker.cook()
        json_feeds.append(json_feed)
        atom_feeds.append(atom_feed)
        write_to_file(f"{normalized_name}.json", json_feed)
        write_to_file(f"{normalized_name}.xml", atom_feed)

    generate_opml(json_feeds, "all_opml_with_json_feed.xml")
    generate_opml(atom_feeds, "all_opml_with_atom_feed.xml")
    put_github_action_env("FEED_FILES", "\n".join(all_feed_files))


def generate_opml(feeds: [SyndicationFeed], path: str):
    all_feed_files.add(path)
    with open(path, 'w') as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
<head>
<title>Feed Cooker</title>
</head>
<body>
""")
        f.write("""<outline title="Cooker" text="Cooker">\n""")
        for feed in feeds:
            url = xml_escape(feed.feed["feed_url"])
            title = xml_escape(feed.feed["title"])
            f.write(
                f"""    <outline text="{title}" type="rss" xmlUrl="{url}" title="{title}"/>\n""")
        f.write("</outline>\n")
        f.write("</body>\n")
        f.write("</opml>\n")


def write_to_file(path: str, feed: SyndicationFeed):
    all_feed_files.add(path)
    with open(path, "w") as f:
        feed.write(f, "utf-8")


if __name__ == "__main__":
    fire.Fire(main)
