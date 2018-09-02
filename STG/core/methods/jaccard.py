from core.methods.interface import Method


class Jaccard(Method):
    def __init__(self):
        self.first_tokens = None
        self.second_tokens = None

    def score(self, w1: str, w2: str) -> float:
        self.first_tokens = self._build_tokens(word=w1)
        self.second_tokens = self._build_tokens(word=w2)

        intersection_cardinality = float(len(self.intersection))
        union_cardinality = float(len(self.union))

        return intersection_cardinality / union_cardinality

    @property
    def intersection(self) -> set:
        return set.intersection(self.first_tokens, self.second_tokens)

    @property
    def union(self) -> set:
        return set.union(self.first_tokens, self.second_tokens)

    @staticmethod
    def _build_tokens(word: str) -> set:
        return set(word)
