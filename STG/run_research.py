import argparse
import configparser

from core import methods

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')

    allowed_methods = {
        'sorensen': methods.Sorensen(
            count=config['Sorensen']['NGramSize']
        ),
        'jaro_winkler': methods.JaroWinkler(
            scaling=config['JaroWinkler']['Scaling']
        ),
        'jaro': methods.Jaro(),
        'jaccard': methods.Jaccard()
    }

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--first',
        help='Word a',
        required=True,
        type=str
    )
    parser.add_argument(
        '-s',
        '--second',
        help='Word b',
        required=True,
        type=str
    )

    args = parser.parse_args()

    print('*' * 20)
    print('First:', args.first, '|', 'Second:', args.second)

    for name, method in allowed_methods.items():
        name = name.upper().replace('_', ' ')
        score = method.score(
            w1=args.first, w2=args.second
        )
        print('- ', name, '|', score)
    print('*' * 20)
