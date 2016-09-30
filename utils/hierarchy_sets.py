from collections import defaultdict

class HierarchySets(object):

    def __init__(
        self,
        parent_child_tuples
    ):

        # ancestor_to_descendants
        a2ds = defaultdict(set)

        # descendant_to_ancestors
        d2as = defaultdict(set)

        for pct in parent_child_tuples:
            if pct[0] is None:
                continue
            a2ds[pct[0]].add(pct[1])
            d2as[pct[1]].add(pct[0])

            if pct[0] in d2as:
                for ancestor in d2as[pct[0]]:
                    a2ds[ancestor].add(pct[1])
                    d2as[pct[1]].add(ancestor)

        self._a2ds = a2ds
        self._d2as = d2as

    def descendants(self, ancestor):
        if ancestor in self._a2ds:
            return self._a2ds[ancestor]
        return set()

    def ancestors(self, descendant):
        if descendant in self._d2as:
            return self._d2as[descendant]
        return set()

    def is_decendant(self, descendant, ancestor):
        return descendant in self._a2ds[ancestor]

    def is_ancestor(self, ancestor, descendant):
        return ancestor in self._d2as[ancestor]
