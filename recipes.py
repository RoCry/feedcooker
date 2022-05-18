import operator
from functools import reduce

import listparser

_recipes = {
    # you need change the name, demo will be ignored by default
    "demo": {
        "urls": [
            "https://aws.amazon.com/blogs/big-data/feed/",
        ],
        ######################################################################
        # optional
        "filters": [
            {
                "title": "EMR|AWS|Big Data|Amazon|ETL|ML|Amazon",  # regex to match title
            },
            {
                "in_seconds": 3600
                * 24
                * 7,  # only the items published in the last 7 days will show
            },
        ],
        ######################################################################
    },
}


def get_recipes() -> [dict]:
    recipes = {}
    for name, recipe in _recipes.items():
        for sub_name, r in _fulfill_opml_recipe(name, recipe).items():
            recipes[sub_name] = r
    return recipes


# change the recipe with opml url to multi recipes
def _fulfill_opml_recipe(name: str, recipe: dict) -> dict:
    if "opml" not in recipe:
        return {name: recipe}

    result = listparser.parse(recipe["opml"])
    del recipe["opml"]

    feeds = {}
    for f in result.feeds:
        categories = (
            ["uncategorized"]
            if not f.categories
            else reduce(operator.concat, f.categories)
        )
        for c in categories:
            feeds[c] = feeds.get(c, []) + [f.url]

    results = {}
    all_urls = set()
    for key, urls in feeds.items():
        r = recipe.copy()
        r["urls"] = urls
        all_urls.update(urls)
        results[f"{name}_{key}"] = r
    results[name] = all_urls
    return results
