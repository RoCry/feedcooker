import datetime

from filter import Filter


def test_title_filter():
    f = Filter.from_dict(title="foo")
    assert f.predicate_item({"title": "foo"})
    assert not f.predicate_item({"title": "bar"})
    assert f.predicate_item({"title": "Foo"})

    f = Filter.from_dict(title="FoO")
    assert f.predicate_item({"title": "foo"})
    assert not f.predicate_item({"title": "bar"})
    assert f.predicate_item({"title": "Foo"})


def test_title_filter_title_sensitive():
    f = Filter.from_dict(title="foo", case_sensitive=True, invert=False)
    assert f.predicate_item({"title": "foo"})
    assert not f.predicate_item({"title": "Foo"})


def test_title_filter_title_invert():
    f = Filter.from_dict(title="foo", case_sensitive=False, invert=True)
    assert not f.predicate_item({"title": "foo"})
    assert f.predicate_item({"title": "bar"})
    assert not f.predicate_item({"title": "Foo"})


def test_time_filter():
    now = datetime.datetime.now()

    f = Filter.from_dict(in_seconds=10)
    assert f.predicate_item({"pubdate": now})
    assert not f.predicate_item({})
    assert not f.predicate_item({"pubdate": now - datetime.timedelta(seconds=11)})


def test_filters_from_dicts():
    ds = [
        {"title": "foo"},
        {"in_seconds": 1},
    ]

    filters = Filter.from_dicts(ds)
    assert len(filters) == 2

    filters = Filter.from_dicts(None)
    assert len(filters) == 0

    filters = Filter.from_dicts([])
    assert len(filters) == 0
