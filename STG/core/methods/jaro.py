import math

from core.methods.interface import Method


class Jaro(Method):
    def score(self, w1: str, w2: str) -> float:
        shorter, longer = w1.lower(), w2.lower()

        if len(w1) > len(w2):
            longer, shorter = shorter, longer

        m1 = self.build_matching_characters(w1=shorter, w2=longer)
        m2 = self.build_matching_characters(w1=longer, w2=shorter)

        if len(m1) == 0 or len(m2) == 0:
            return 0.0

        return (float(len(m1)) / len(shorter) +
                float(len(m2)) / len(longer) +
                float(len(m1) - self.transpositions(w1=m1, w2=m2)) / len(m1)) / 3.0

    @staticmethod
    def transpositions(w1: str, w2: str) -> float:
        return math.floor(len([(f, s) for f, s in zip(w1, w2) if not f == s]) / 2.0)

    @staticmethod
    def build_matching_characters(w1: str, w2: str) -> str:
        tmp = w2
        common = []
        limit = math.floor(min(len(w1), len(w2)) / 2)

        for i, l in enumerate(w1):
            left, right = int(max(0.0, i - limit)), int(min(i + limit + 1, len(tmp)))
            if l in tmp[left:right]:
                common.append(l)
                tmp = tmp[0:tmp.index(l)] + '*' + tmp[tmp.index(l) + 1:]

        return ''.join(common)
