import operator
from functools import reduce

import listparser

# change the demo recipe to what you want to use
_recipes = {
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


def get_recipes(prefer_submirror=True) -> [dict]:
    recipes = {}
    for name, recipe in _recipes.items():
        for sub_name, r in _fulfill_opml_recipe(name, recipe).items():
            recipes[sub_name] = r
    if prefer_submirror:
        for recipe in recipes.values():
            _transform_to_submirror(recipe)
    return recipes


def _transform_to_submirror(r: dict):
    for i, u in enumerate(r["urls"]):
        r["urls"][i] = _transform_url_to_submirror(u)


def _transform_url_to_submirror(u: str) -> str:
    from urllib.parse import urlparse
    o = urlparse(u)
    if not o.path.endswith("/feed/atom"):
        return u
    if not o.hostname.endswith("mirror.xyz"):
        return u
    return u.replace("mirror.xyz", "submirror.xyz").rstrip("/feed/atom")


def test_transform_url_to_submirror():
    assert _transform_url_to_submirror(
        "https://mirror.xyz/0xBE4fde70B16d2dD454Fa8434E1A01131b90D2880/feed/atom") == "https://submirror.xyz/0xBE4fde70B16d2dD454Fa8434E1A01131b90D2880"
    assert _transform_url_to_submirror("https://dev.mirror.xyz/feed/atom") == "https://dev.submirror.xyz"
    assert _transform_url_to_submirror("https://optoutpod.com/blog/feed") == "https://optoutpod.com/blog/feed"
    assert _transform_url_to_submirror("https://rocry.com/feed/atom") == "https://rocry.com/feed/atom"


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

    r = recipe.copy()
    r["urls"] = list(all_urls)
    results[name] = r
    return results
