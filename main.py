from feedgenerator import SyndicationFeed

from recipes import get_recipes
from cooker import Cooker
import fire

from util import url_to_valid_filename, put_github_action_env


def main(repository: str, repository_owner: str, limit=20):
    recipes = get_recipes()

    feed_files = []
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
        json_feed_file = f"{normalized_name}.json"
        atom_feed_file = f"{normalized_name}.xml"
        write_to_file(json_feed_file, json_feed)
        write_to_file(atom_feed_file, atom_feed)
        feed_files.append(json_feed_file)
        feed_files.append(atom_feed_file)

    put_github_action_env("FEED_FILES", "\n".join(feed_files))


def write_to_file(path: str, feed: SyndicationFeed):
    with open(path, "w") as f:
        feed.write(f, "utf-8")


if __name__ == "__main__":
    fire.Fire(main)
