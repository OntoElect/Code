#!/usr/bin/env python2
#encoding: UTF-8

# reads clean text files from directory
# and and writes combined datasets into another directory

import ate3 as ate
import argparse
import time
from os import listdir
from os.path import isfile, join
import os
import psutil

t0 = time.time()

parser = argparse.ArgumentParser()

parser.add_argument("--in_txt_dir", help="input directory containing clean TXT files")
parser.add_argument("--out_dataset_dir", help="output directory containing datasets")
parser.add_argument("--strategy", default='time-desc', help="strategy of dataset generation: time-asc|time-desc|random|time-bidir|citation-desc")
parser.add_argument("--citations", default=False, help="csv file that contains citations as (number,filename) pairs per row ")
parser.add_argument("--increment_size", default=20, help="number of TXT files to incrementally generate datasets")

args = parser.parse_args()

in_txt_dir=args.in_txt_dir
out_dataset_dir=args.out_dataset_dir
strategy=args.strategy
citations=args.citations
increment_size=int(args.increment_size)

print("reading raw TXT from",in_txt_dir, "writing datasets to", out_dataset_dir)

ate.compose_datasets(in_txt_dir, out_dataset_dir, increment_size=increment_size, increment_strategy=strategy,citations=citations)

t1 = time.time()
print "finished in ", t1 - t0, " seconds "

process = psutil.Process(os.getpid())
print(process.memory_info().rss)  # in bytes 
