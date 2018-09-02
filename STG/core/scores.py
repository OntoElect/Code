from typing import (
    List,
    Dict
)

from core.models import Token


def thd(current_groups: Dict[str, Token], previous_groups: Dict[str, Token]) -> float:
    result = 0.0

    for group_key, token in current_groups.items():
        previous_group = previous_groups.get(group_key, None)

        if previous_group is not None:
            result += abs(
                token.value - previous_group.value
            )
        else:
            result += token.value

    return result


def thdr(thd_value: float, sum_norm: float) -> float:
    return thd_value / sum_norm * 100.0


def eps(tokens: List[Token], criterion: float) -> Token or None:
    score_sum = 0.0
    score_total = sum((token.value for token in tokens))

    last = len(tokens) - 2

    for i, token in enumerate(tokens):
        score_sum += token.value

        score_a = score_sum / score_total

        if i != last and score_a >= criterion:
            score_b = tokens[i + 1]
            score_c = tokens[i + 2]

            if score_b.value != score_c.value:
                return score_b
    return None
