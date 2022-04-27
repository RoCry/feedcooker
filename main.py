from recipes import recipes
from cooker import Cooker
import fire


def main(repository: str, repository_owner: str, limit=10):
    for name in recipes:
        cooker = Cooker(
            name=name,
            repository=repository,
            repository_owner=repository_owner,
            recipe=recipes[name],
            limit=limit,
        )
        json_feed, atom_feed = cooker.cook()
        with open(f"./well-done/{name}.json", "w") as f:
            json_feed.write(f, "utf-8")
        with open(f"./well-done/{name}.atom.xml", "w") as f:
            atom_feed.write(f, "utf-8")


if __name__ == "__main__":
    fire.Fire(main)
