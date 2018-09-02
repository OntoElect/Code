from collections import OrderedDict
from typing import List

from core import (
    scores,
    files,
    terms
)
from core.decorators import timeit
from core.methods import Method


def term_madrid(
        files_list: List,
        method: Method,
        convergence: float
):
    @timeit
    def read_tokens(input_file):
        return list(
            files.read_file(
                filename=input_file.path
            )
        )

    @timeit
    def more_than_one(tokens):
        return terms.where(
            tokens=tokens,
            attribute='value',
            operator='gt',  # >
            criterion=1.0,
            orderby='value'
        )

    @timeit
    def eps(tokens):
        return scores.eps(
            tokens=tokens,
            criterion=0.5
        )

    @timeit
    def more_than_eps(tokens, eps_value):
        return terms.where(
            tokens=tokens,
            attribute='value',
            operator='ge',  # >=
            criterion=eps_value,
            orderby='value'
        )

    @timeit
    def normalized(tokens):
        return list(terms.normalize(
            tokens=tokens
        ))

    @timeit
    def build_groups(tokens, method_obj, convergence_value):
        return terms.build_groups(
            normalized_tokens=tokens,
            method=method_obj,
            convergence=convergence_value
        )

    @timeit
    def sum_normalized(tokens_groups):
        return sum((token.value for token in tokens_groups.values()))

    @timeit
    def calculate_thd(tokens_groups, prev_tokens_groups):
        return scores.thd(
            current_groups=tokens_groups,
            previous_groups=prev_tokens_groups
        )

    @timeit
    def calculate_thdr(thd_calculated, sum_norm_calculated):
        return scores.thdr(
            thd_value=thd_calculated,
            sum_norm=sum_norm_calculated
        )

    prev_groups = None

    for file in files_list:
        step_0_time, input_tokens = read_tokens(
            input_file=file
        )
        step_1_time, step_1 = more_than_one(
            tokens=input_tokens
        )
        step_2_time, step_2 = eps(
            tokens=step_1
        )
        step_3_time, step_3 = more_than_eps(
            tokens=step_1,
            eps_value=step_2.value
        )
        step_4_time, step_4 = normalized(
            tokens=step_3
        )
        groups_time, groups = build_groups(
            tokens=step_4,
            method_obj=method,
            convergence_value=convergence
        )
        sum_norm_time, sum_norm = sum_normalized(
            tokens_groups=groups
        )

        thd_time = 0.0
        thdr_time = 0.0

        thd_value = sum_norm
        thdr_value = 100.0

        if prev_groups is not None:
            thd_time, thd_value = calculate_thd(
                tokens_groups=groups,
                prev_tokens_groups=prev_groups
            )
            thdr_time, thdr_value = calculate_thdr(
                thd_calculated=thd_value,
                sum_norm_calculated=sum_norm
            )

        prev_groups = groups

        yield OrderedDict([
            ('NAME', file.name),
            ('TERMS COUNT', len(input_tokens)),
            ('MORE THAN ONE', len(step_1)),
            ('MORE THAN EPS', len(step_3)),
            ('EPS', step_2.value),
            ('SUM Norm', sum_norm),
            ('CONVERGENCE', convergence),
            ('GROUPS COUNT', len(groups)),
            ('GROUPS TIME (SEC)', groups_time),
            ('THD', thd_value),
            ('THD TIME (SEC)', thd_time),
            ('THDR', thdr_value),
            ('THDR TIME (SEC)', sum_norm_time + thdr_time)
            # ('TOKENS READ TIME (SEC)', step_0_time),
            # ('MORE THAN ONE TIME (SEC)', step_1_time),
            # ('EPS TIME (SEC)', step_2_time),
            # ('MORE THAN EPS TIME (SEC)', step_3_time),
            # ('NORMALIZATION TIME (SEC)', step_4_time),
            # ('GROUPS TIME (SEC)', groups_time),
            # ('SUM OF NORMALIZED TIME (SEC)', sum_norm_time),
            # ('THD TIME (SEC)', thd_time),
            # ('THDR TIME (SEC)', thdr_time),
        ])
