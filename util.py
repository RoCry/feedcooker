import logging
import os
import pickle
from typing import Optional

import requests

logging.basicConfig(
    level=os.environ.get("LOGLEVEL", logging.INFO),
    format="%(asctime)s %(name)s - [%(levelname)s] > %(message)s",
)
logger = logging.getLogger("feedcooker")

cache_folder = "./downloads"


def url_to_valid_filename(url: str) -> str:
    return url.replace("/", "_").replace(":", "_").replace("?", "_")


def try_load_resp(url: str) -> Optional[requests.Response]:
    key = url_to_valid_filename(url)
    try:
        with open(os.path.join(cache_folder, key), "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


def save_resp(resp: requests.Response):
    os.makedirs(cache_folder, exist_ok=True)

    key = url_to_valid_filename(resp.url)
    with open(os.path.join(cache_folder, key), "wb") as f:
        pickle.dump(resp, f)
