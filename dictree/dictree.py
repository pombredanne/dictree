# coding:utf-8

from collections import MutableMapping
from .labels import WILDCARD, NO_ITEM


class Dictree(MutableMapping):
    def __init__(self):
        self._item = NO_ITEM
        self._subtrees = {}

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, value):
        self._item = value

    @item.deleter
    def item(self):
        self._item = NO_ITEM

    @property
    def has_item(self):
        return self.item is not NO_ITEM

    @property
    def has_subtree(self):
        return len(self._subtrees) != 0

    def __len__(self):
        n = sum(len(t) for t in self._subtrees.values())
        return n + 1 if self.has_item else n

    def __iter__(self):
        if self.has_item:
            yield ()

        for k, t in self._subtrees.items():
            for l in t:
                yield (k,) + l

    def __contains__(self, key):
        if len(key) == 0:
            return self.has_item

        else:
            head, tail = key[0], key[1:]
            if head in self._subtrees:
                return tail in self._subtrees[head]

            else:
                return False

    def __getitem__(self, key):
        try:
            return self.__getitem(key)

        except KeyError:
            raise KeyError(key)

    def __getitem(self, key):
        if len(key) == 0:
            if self.has_item:
                return self.item

            else:
                raise KeyError()

        else:
            head, tail = key[0], key[1:]
            try:
                return self._subtrees[head].__getitem(tail)

            except KeyError:
                return self._subtrees[WILDCARD].__getitem(tail)

    def __setitem__(self, key, item):
        if len(key) == 0:
            self.item = item

        else:
            head, tail = key[0], key[1:]
            self._subtrees.setdefault(head, self.__class__())[tail] = item

    def __delitem__(self, key):
        try:
            return self.__delitem(key)

        except KeyError:
            raise KeyError(key)

    def __delitem(self, key):
        if len(key) == 0:
            if self.has_item:
                del self.item
                return not self.has_subtree

            else:
                raise KeyError()

        else:
            head, tail = key[0], key[1:]
            if self._subtrees[head].__delitem(tail):
                del self._subtrees[head]

            return not self.has_subtree and not self.has_item

    def setdefault(self, key, default):
        if key in self:
            return self[key]

        else:
            self[key] = default
            return default

    def find(self, key, strict=False):
        try:
            return self._find(key, strict)

        except:
            raise KeyError(key)

    def _find(self, key, strict):
        if len(key) == 0:
            if self.has_item:
                return self.item, ()

            else:
                raise KeyError()

        else:
            head, tail = key[0], key[1:]
            try:
                item, trace = self._subtrees[head]._find(tail, strict)
                return item, (False,) + trace

            except KeyError:
                try:
                    item, trace = self._subtrees[WILDCARD]._find(tail, strict)
                    return item, (True,) + trace

                except KeyError:
                    if strict:
                        raise KeyError()

                    else:
                        return self._find((), strict)
