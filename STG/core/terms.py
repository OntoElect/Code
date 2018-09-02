from operator import attrgetter

from typing import (
    Iterator,
    List,
    Dict
)

from core.methods import Method
from core.models import Token


def build_groups(
        normalized_tokens: List[Token],
        method: Method,
        convergence: float
) -> Dict[str, Token]:
    groups = dict()

    while len(normalized_tokens) > 0:
        group_key = normalized_tokens.pop(0)
        group_variants = [group_key]

        for i in range(len(normalized_tokens) - 1, -1, -1):
            score = method.score(
                w1=normalized_tokens[i].term,
                w2=group_key.term
            )

            if score >= convergence:
                group_token = normalized_tokens.pop(i)
                group_token.convergence = score

                group_variants.append(group_token)

            group_value = sum((x.value for x in group_variants))
            group_value = group_value / float(len(group_variants))

            groups[group_key.term] = Token(
                term=group_key.term,
                value=group_value
            )

    return groups


def where(
        tokens: Iterator[Token],
        attribute: str,
        operator: str,
        criterion: float,
        orderby: str,
        reverse: bool = True,
) -> List[Token]:
    if operator not in ['ge', 'gt', 'le', 'lt', 'eq', 'ne']:
        raise ValueError('Operator not found')

    operator = '__{operator}__'.format(
        operator=operator
    )

    generator = (
        token for token in tokens
        if getattr(getattr(token, attribute), operator)(criterion)
    )

    return sorted(generator, key=attrgetter(orderby), reverse=reverse)


def normalize(tokens: Iterator[Token]) -> Iterator[Token]:
    max_score = max((token.value for token in tokens))

    for token in tokens:
        yield Token(
            term=token.term,
            value=token.value / max_score
        )
