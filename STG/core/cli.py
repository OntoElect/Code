import argparse

from typing import Dict


def read_args(methods: Dict):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--method',
        help='Specify method name',
        choices=methods.keys(),
        required=True
    )
    parser.add_argument(
        '-c',
        '--convergence',
        help='Specify a convergence value',
        type=float,
        required=True
    )
    return parser.parse_args()


def show_results(*args):
    print()
    print('*' * 50)
    print('File:', args[0])
    print()
    print('Terms:')
    print('- TOTAL:', args[1])
    print('- MORE THAN 1:', args[2])
    print('- MORE THAN EPS:', args[3])
    print()
    print('Info:')
    print('- EPS:', args[4])
    print('- NORM:', args[5])
    print('- CONVERGENCE:', args[6])
    print('- GROUPS:', args[7])
    print('- THD:', args[9])
    print('- THDR:', args[11])
    print()
    print('Time (seconds):')
    print('- GROUPS:', args[8])
    print('- THD:', args[10])
    print('- THDR:', args[12])

    print('*' * 50)
