# coding:utf-8

import pytest
from dictree import Dictree, WILDCARD


def instanciate():
    e = Dictree()
    e[1, 2, 3, 4] = 100
    e[1, 2, 3, 5] = 200
    e[1, 2, 3, WILDCARD] = 300
    e[1, 2, 3] = 10
    e[1, 2, 4] = 20
    e[1, WILDCARD] = 100
    e[1, WILDCARD, 5] = 400
    e[1, 10, WILDCARD, 6] = 500
    return e


def raises_keyerror(f, key):
    try:
        f()
    except KeyError as e:
        assert e.args[0] == key
    else:
        assert False


def test_len():
    elt = Dictree()
    elt[1, 2] = 2
    elt[1, 3] = 3
    elt[1, 3, 4] = 4
    elt[1, 3, 5] = 5
    assert len(elt) == 4


def test_contains():
    elt = Dictree()
    elt[1, 2] = 2
    elt[1, WILDCARD] = 4
    assert (1, 2) in elt
    assert (1, WILDCARD) in elt
    assert (1, 4) not in elt
    assert (1,) not in elt


def test_iter():
    elt = Dictree()
    elt[1, 2] = 2
    elt[1, WILDCARD] = 3
    keys = [k for k in elt]
    assert (1, 2) in keys
    assert (1, WILDCARD) in keys
    assert len(keys) == 2


def test_get():
    elt = Dictree()
    elt[1, 2] = 2
    elt[1, WILDCARD] = 3
    assert elt[1, 2] == 2
    assert elt[1, 3] == 3


def test_get_keyerror():
    elt = Dictree()
    elt[1, 2, 3] = 2
    elt[1, 2, WILDCARD] = 3
    elt[1, 3] = 4

    raises_keyerror(lambda: elt[(1,)], (1,))
    raises_keyerror(lambda: elt[(1, 2, 3, 4)], (1, 2, 3, 4))
    raises_keyerror(lambda: elt[(1, 2, 4, 5)], (1, 2, 4, 5))


def test_del():
    elt = Dictree()
    elt[1, 2, 3] = 2
    elt[(1,)] = 3
    del elt[1, 2, 3]
    assert len(elt) == 1

    elt = Dictree()
    elt[1, 2, 3] = 1
    del elt[1, 2, 3]
    assert len(elt) == 0


def test_del_keyerror():
    elt = Dictree()
    elt[1, 2, 3] = 1
    elt[1, 2, WILDCARD] = 2

    raises_keyerror(lambda: elt.__delitem__((1, 2, 4)), (1, 2, 4))
    raises_keyerror(lambda: elt.__delitem__((1, 2)), (1, 2))


def test_find():
    elt = Dictree()
    elt[1, 2] = 1
    assert elt.find((1, 2, 3)) == (1, (False, False))
    assert elt.find((1, 2)) == (1, (False, False))

    elt = Dictree()
    elt[1, WILDCARD] = 1
    elt[1, WILDCARD, 2, 3] = 2
    assert elt.find((1, 2)) == (1, (False, True))
    assert elt.find((1, 3, 2)) == (1, (False, True))

    elt = Dictree()
    elt[2, 3] = 0
    elt[WILDCARD, 1, 2] = 1
    elt[WILDCARD, 2, 3] = 2
    assert elt.find((2, 1, 2)) == (1, (True, False, False))


def test_find_keyerror():
    elt = Dictree()
    elt[2, 3] = 0
    elt[WILDCARD, 1, 2] = 1
    elt[WILDCARD, 2, 3] = 2
    raises_keyerror(lambda: elt.find((1, 1)), (1, 1))
    raises_keyerror(lambda: elt.find((1, 1, 2, 3), True), (1, 1, 2, 3))
