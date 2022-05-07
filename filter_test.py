import datetime

from filter import TitleFilter, TimeFilter


def test_title_filter():
    f = TitleFilter(pattern="foo", case_sensitive=False, invert=False)
    assert f.predicate_item({"title": "foo"})
    assert not f.predicate_item({"title": "bar"})
    assert f.predicate_item({"title": "Foo"})

    f = TitleFilter(pattern="FoO", case_sensitive=False, invert=False)
    assert f.predicate_item({"title": "foo"})
    assert not f.predicate_item({"title": "bar"})
    assert f.predicate_item({"title": "Foo"})


def test_title_filter_title_sensitive():
    f = TitleFilter(pattern="foo", case_sensitive=True, invert=False)
    assert f.predicate_item({"title": "foo"})
    assert not f.predicate_item({"title": "Foo"})


def test_title_filter_title_invert():
    f = TitleFilter(pattern="foo", case_sensitive=False, invert=True)
    assert not f.predicate_item({"title": "foo"})
    assert f.predicate_item({"title": "bar"})
    assert not f.predicate_item({"title": "Foo"})


def test_time_filter():
    now = datetime.datetime.now()

    f = TimeFilter(in_seconds=10)
    assert f.predicate_item({"pubdate": now})
    assert not f.predicate_item({})
    assert not f.predicate_item({"pubdate": now - datetime.timedelta(seconds=11)})
