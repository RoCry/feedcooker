from recipes import recipes
from cooker import Cooker
import fire


def main(repository: str, repository_owner: str):
    for name in recipes:
        cooker = Cooker(
            name=name,
            repository=repository,
            repository_owner=repository_owner,
            recipe=recipes[name],
        )
        feed = cooker.cook()
        with open(f"./well-done/{name}.json", "w") as f:
            feed.write(f, "utf-8")


if __name__ == "__main__":
    fire.Fire(main)
