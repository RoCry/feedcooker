from recipes import get_recipes
from cooker import Cooker
import fire

from util import url_to_valid_filename


def main(repository: str, repository_owner: str, limit=20):
    recipes = get_recipes()

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
        with open(f"./well-done/{normalized_name}.json", "w") as f:
            json_feed.write(f, "utf-8")
        with open(f"./well-done/{normalized_name}.atom.xml", "w") as f:
            atom_feed.write(f, "utf-8")


if __name__ == "__main__":
    fire.Fire(main)
