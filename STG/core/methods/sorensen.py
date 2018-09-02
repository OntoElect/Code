from core.methods.interface import Method


class Sorensen(Method):
    def __init__(self, count: int = 2):
        self.count = int(count)
        self.first_tokens = None
        self.second_tokens = None

    def score(self, w1: str, w2: str) -> float:
        self.first_tokens = self._build_tokens(
            word=w1, count=self.count
        )
        self.second_tokens = self._build_tokens(
            word=w2, count=self.count
        )

        if not self.total:
            return 0.0
        return float(len(self.intersection) * self.count) / float(self.total)

    @property
    def intersection(self) -> set:
        return set.intersection(self.first_tokens, self.second_tokens)

    @property
    def total(self) -> int:
        return len(self.first_tokens) + len(self.second_tokens)

    @staticmethod
    def _build_tokens(word: str, count: int) -> set:
        def transform(value, s, e):
            return value[s:e]

        size = len(word) - (count - 1)
        tokens = {transform(word, i, i + count) for i in range(0, size)}

        return tokens
