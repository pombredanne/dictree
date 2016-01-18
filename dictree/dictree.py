# coding:utf-8

from collections import MutableMapping
from .labels import WILDCARD, ITEM


class Dictree(MutableMapping):
    def __init__(self):
        self._data = {}

    def __contains__(self, key):
        head = self._data
        for k in key:
            if k in head:
                head = head[k]

            else:
                return False

        return ITEM in head

    def __len__(self):
        n = 0
        stack = [self._data]
        while stack:
            d = stack.pop(-1)
            stack.extend([v for k, v in d.items() if k is not ITEM])
            if ITEM in d:
                n += 1

        return n

    def __iter__(self):
        stack = [((), self._data)]
        while stack:
            prefix, dic = stack.pop(-1)
            for k, v in dic.items():
                if k is ITEM:
                    yield prefix

                else:
                    path = prefix + (k,)
                    stack.append((path, v))

    def __getitem__(self, key):
        return self.find(key)[0]

    def __setitem__(self, key, value):
        head = self._data
        for k in key:
            if k in head:
                head = head[k]

            else:
                head = head.setdefault(k, {})

        head[ITEM] = value

    def __delitem__(self, key):
        stack = []
        head = self._data
        for k in key:
            if k in head:
                stack.append((k, head))
                head = head[k]

            else:
                raise KeyError(key)

        if ITEM in head:
            del head[ITEM]
            blank = len(head) == 0
            while blank and stack:
                k, d = stack.pop(-1)
                del d[k]
                blank = len(d) == 0

        else:
            raise KeyError(key)

    def setdefault(self, key, default):
        if key in self:
            return self[key]

        else:
            self[key] = default
            return default

    def find(self, key):
        trace = []
        head = self._data
        for k in key:
            if k in head:
                trace.append(False)
                head = head[k]

            elif WILDCARD in head:
                trace.append(True)
                head = head[WILDCARD]

            else:
                raise KeyError(key)

        if ITEM in head:
            return head[ITEM], tuple(trace)

        else:
            raise KeyError(key)
