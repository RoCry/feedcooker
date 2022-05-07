recipes = {
    # you need change the name, demo will be ignored by default
    "demo": {
        "urls": [
            "https://aws.amazon.com/blogs/big-data/feed/",
        ],
        ######################################################################
        # optional
        "filter": {
            "title": "EMR|AWS|Big Data|Amazon|ETL|ML|Amazon",  # regex to match title
            "in_seconds": 3600
            * 24
            * 7,  # only the items published in the last 7 days will show
        },
        ######################################################################
    },
}
