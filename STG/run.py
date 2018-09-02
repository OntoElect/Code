import configparser
import datetime
import csv
import os

from core import (
    methods,
    files,
    algo,
    cli
)

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

    args = cli.read_args(
        methods=allowed_methods
    )

    current_folder = os.path.dirname(os.path.abspath(__file__))

    input_files = files.load_list(
        path=current_folder,
        folder=config['IO']['InputFolder']
    )

    output_filename = 'results_date({date})_method({method})_files({size})'.format(
        method=args.method,
        date=datetime.datetime.now().date(),
        size=len(input_files)
    )

    output_file = '{path}{slash}{folder}{slash}{name}.csv'.format(
        path=current_folder,
        folder=config['IO']['OutputFolder'],
        name=output_filename,
        slash=files.system_slash()
    )

    method = allowed_methods[args.method]

    results = algo.term_madrid(
        files_list=input_files,
        method=method,
        convergence=float(args.convergence)
    )

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')

        for i, result in enumerate(results):
            if i == 0:
                writer.writerow(result.keys())

            output = result.values()

            # File
            writer.writerow(output)
            # Console
            cli.show_results(*output)
