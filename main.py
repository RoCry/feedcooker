import json

from feeds_config import feeds_cfg
from cooker import Cooker


def main():
    cooker = Cooker(feeds_cfg)

    feed = cooker.cook()
    with open("./feeds.gen.json", "w") as f:
        feed.write(f, "utf-8")


if __name__ == "__main__":
    main()
