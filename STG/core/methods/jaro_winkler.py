from core.methods.jaro import Jaro


class JaroWinkler(Jaro):
    def __init__(
            self,
            scaling: float = 0.1
    ):
        self.scaling = float(scaling)

    def score(self, w1: str, w2: str) -> float:
        jaro = super().score(
            w1=w1,
            w2=w2
        )

        if jaro < 0.7:
            return jaro
        else:
            cl = min(len(self.get_prefix(w1, w2)), 4)

            return ((jaro + (self.scaling * cl * (1.0 - jaro))) * 100.0) / 100.0

    def get_prefix(self, w1: str, w2: str) -> str:
        index = self.get_diff_index(w1, w2)

        if index == -1:
            return w1

        elif index == 0:
            return ''

        return w1[0:index]

    @staticmethod
    def get_diff_index(w1: str, w2: str) -> int:
        if w1 == w2:
            return -1

        max_len = min(len(w1), len(w2))
        for i in range(0, max_len):
            if not w1[i] == w2[i]:
                return i

        return max_len
