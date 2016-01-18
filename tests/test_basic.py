# coding:utf-8

import pytest
from dictree import Dictree, WILDCARD


def instanciate():
    dt = Dictree()
    dt[1, 2, 3, 4] = 100
    dt[1, 2, 3, 5] = 200
    dt[1, 2, 3, WILDCARD] = 300
    dt[1, 2, 3] = 10
    dt[1, 2, 4] = 20
    dt[1, WILDCARD] = 100
    dt[1, WILDCARD, 5] = 400
    dt[1, 10, WILDCARD, 6] = 500
    return dt


def raises_keyerror(f, key):
    try:
        f()
    except KeyError as e:
        assert e.args[0] == key
    else:
        assert False


def test_len():
    dt = Dictree()
    dt[1, 2] = 2
    dt[1, 3] = 3
    dt[1, 3, 4] = 4
    dt[1, 3, 5] = 5
    assert len(dt) == 4


def test_contains():
    dt = Dictree()
    dt[1, 2] = 2
    dt[1, WILDCARD] = 4
    assert (1, 2) in dt
    assert (1, WILDCARD) in dt
    assert (1, 4) not in dt
    assert (1,) not in dt


def test_iter():
    dt = Dictree()
    dt[1, 2] = 2
    dt[1, WILDCARD] = 3
    keys = [k for k in dt]
    assert (1, 2) in keys
    assert (1, WILDCARD) in keys
    assert len(keys) == 2


def test_get():
    dt = Dictree()
    dt[1, 2] = 2
    dt[1, WILDCARD] = 3
    assert dt[1, 2] == 2
    assert dt[1, 3] == 3


def test_get_keyerror():
    dt = Dictree()
    dt[1, 2, 3] = 2
    dt[1, 2, WILDCARD] = 3
    dt[1, 3] = 4

    raises_keyerror(lambda: dt[(1,)], (1,))
    raises_keyerror(lambda: dt[(1, 2, 3, 4)], (1, 2, 3, 4))
    raises_keyerror(lambda: dt[(1, 2, 4, 5)], (1, 2, 4, 5))


def test_del():
    dt = Dictree()
    dt[1, 2, 3] = 2
    dt[(1,)] = 3
    del dt[1, 2, 3]
    assert len(dt) == 1

    dt = Dictree()
    dt[1, 2, 3] = 1
    del dt[1, 2, 3]
    assert len(dt) == 0


def test_del_keyerror():
    dt = Dictree()
    dt[1, 2, 3] = 1
    dt[1, 2, WILDCARD] = 2

    raises_keyerror(lambda: dt.__delitem__((1, 2, 4)), (1, 2, 4))
    raises_keyerror(lambda: dt.__delitem__((1, 2)), (1, 2))


def test_find():
    dt = Dictree()
    dt[1, 2] = 1
    assert dt.find((1, 2)) == (1, (False, False))


def test_find_keyerror():
    dt = Dictree()
    dt[2, 3] = 0
    dt[WILDCARD, 1, 2] = 1
    dt[WILDCARD, 2, 3] = 2
    raises_keyerror(lambda: dt.find((1, 1)), (1, 1))
    raises_keyerror(lambda: dt.find((1, 1, 2, 3)), (1, 1, 2, 3))


def test_building_a_big_tree_should_not_fail_with_maximum_recursion_error():
    elt = Dictree()
    for x in range(100):
        data = range(1000)
        while data:
            elt[data] = 0
            data.pop(0)
