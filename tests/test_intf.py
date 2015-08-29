# coding:utf-8

from dictree import Dictree, WILDCARD


def instanciate():
    e = Dictree()
    e[1, 2, 3, 4] = 100
    e[1, 2, 3, 5] = 200
    e[1, 2, 3, WILDCARD] = 300
    e[1, 2, 3] = 10
    e[1, 2, 4] = 20
    e[1, WILDCARD] = 30
    return e


def test_popitem():
    e = instanciate()
    key, item = e.popitem()
    assert isinstance(item, int)
    assert len(e) == 5

    for i in range(5):
        e.popitem()

    assert len(e) == 0


def test_pop():
    e = instanciate()
    item = e.pop((1, 2, 3))
    assert item == 10
    assert len(e) == 5


def test_iterkeys():
    e = instanciate()
    if hasattr(e, 'iterkeys'):  # only in python2.x
        assert len([k for k in e.iterkeys()]) == 6


def test_itervalues():
    e = instanciate()
    if hasattr(e, 'itervalues'):  # only in python2.x
        assert sum(i for i in e.itervalues()) == 660


def test_iteritems():
    e = instanciate()
    if hasattr(e, 'iteritems'):  # only in python2.x
        assert sum(i for k, i in e.iteritems()) == 660


def test_keys():
    e = instanciate()
    assert len([k for k in e.keys()]) == 6


def test_values():
    e = instanciate()
    assert sum(i for i in e.values()) == 660


def test_items():
    e = instanciate()
    assert sum(i for k, i in e.items()) == 660


def test_get():
    e = instanciate()
    assert e.get((1, 2, 3, 4)) == 100
    assert e.get((1, 2, 3, 6)) == 300
    assert e.get((1, 2, 5), None) is None


def test_update():
    e1 = instanciate()
    e2 = Dictree()
    e2[1, 2, 3, 4] = -100
    e2[1, 2, 3, 6] = -200
    e2[1, 2, 3] = -300

    e1.update(e2)
    assert len(e1) == 7
    assert e1[1, 2, 3, 4] == -100
    assert e1[1, 2, 3, 6] == -200
    assert e1[1, 2, 3] == -300
    assert e1[1, 2, 3, 7] == 300


def test_setdefault():
    e = instanciate()
    e.setdefault((1, 2, 3, 4), -100)
    e.setdefault((1, 2, 3, 6), -200)
    assert e[1, 2, 3, 4] == 100
    assert e[1, 2, 3, 6] == -200


def test_clear():
    e = instanciate()
    e.clear()
    assert len(e) == 0
