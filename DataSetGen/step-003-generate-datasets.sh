#!/bin/sh
# uncomment one of the lines below to invoke different strategies of dataset generation
# PYTHONPATH=/usr/local/lib/python2.7/dist-packages  python2 step-003-generate-datasets.py --in_txt_dir=data/cleantxt/test --out_dataset_dir=data/datasets/test --strategy=time-asc    --increment_size=20
# PYTHONPATH=/usr/local/lib/python2.7/dist-packages  python2 step-003-generate-datasets.py --in_txt_dir=data/cleantxt/test --out_dataset_dir=data/datasets/test --strategy=time-desc   --increment_size=20
# PYTHONPATH=/usr/local/lib/python2.7/dist-packages  python2 step-003-generate-datasets.py --in_txt_dir=data/cleantxt/test --out_dataset_dir=data/datasets/test --strategy=random      --increment_size=20
PYTHONPATH=/usr/local/lib/python2.7/dist-packages  python2 step-003-generate-datasets.py --in_txt_dir=data/cleantxt/test --out_dataset_dir=data/datasets/test --strategy=time-bidir  --increment_size=20
# PYTHONPATH=/usr/local/lib/python2.7/dist-packages  python2 step-003-generate-datasets.py --in_txt_dir=data/cleantxt/test --out_dataset_dir=data/datasets/test --strategy=citation-desc --increment_size=20 --citations=data/citations/test.xls
