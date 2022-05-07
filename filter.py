import datetime

from regex import regex


class Filter(object):
    def predicate_item(self, item):
        raise NotImplementedError

    def filter_items(self, items):
        return [item for item in items if self.predicate_item(item)]


class TitleFilter(Filter):
    def __init__(self, pattern: str, case_sensitive=False, invert=False):
        self.pattern = regex.compile(pattern if case_sensitive else pattern.lower())
        self.invert = invert
        self.case_sensitive = case_sensitive

    def predicate_item(self, item):
        title = item["title"] if self.case_sensitive else item["title"].lower()
        contains = self.pattern.search(title) is not None
        return contains ^ self.invert


class TimeFilter(Filter):
    def __init__(self, in_seconds: int):
        self.in_seconds = in_seconds

    def predicate_item(self, item):
        if "pubdate" not in item:
            return False

        return item["pubdate"] > datetime.datetime.now() - datetime.timedelta(
            seconds=self.in_seconds
        )
