class Path:
    def __init__(self, path: str, name: str, order: str):
        self.path = path.strip()
        self.name = name.strip()
        self.order = int(order)

    def __repr__(self):
        return 'Path({path}, order={order})'.format(
            order=self.order,
            path=self.path
        )


class Token:
    def __init__(self, term: str, value: float, convergence: float = 0.0):
        self.term = term.strip()
        self.value = float(value)
        self.convergence = float(convergence)

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other):
        return (
            (self.term, self.value, self.convergence) ==
            (other.term, other.value, other.convergence)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self) -> str:
        return 'Token({term}, value={value}, convergence={conv})'.format(
            term=self.term,
            value=self.value,
            conv=self.convergence
        )
