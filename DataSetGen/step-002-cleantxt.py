#!/usr/bin/env python2
#encoding: UTF-8

# reads raw text files from directory
# and writes clean text to another directory

import ate3 as ate
import argparse

from os import listdir
from os.path import isfile, join


parser = argparse.ArgumentParser()

parser.add_argument("--in_txt_dir", help="input directory containing raw TXT files")
parser.add_argument("--out_txt_dir", help="output directory containing clean TXT files")

args = parser.parse_args()

in_txt_dir=args.in_txt_dir
out_txt_dir=args.out_txt_dir

print("reading raw TXT from",in_txt_dir, "writing clean TXT to", out_txt_dir)




raw_txt_files=sorted([ (in_txt_dir, f) for f in listdir(in_txt_dir) if isfile(join(in_txt_dir, f)) and f.lower().endswith(".txt")])
print(raw_txt_files)

for f in raw_txt_files:
    fpath_out=join(out_txt_dir, f[1])
    print(in_txt_dir,'/',f[1],"=>", fpath_out)
    ftxt = open(fpath_out,'w')
    try:
        file_content=ate.clean_text(join(f[0], f[1]))
        ftxt.write(file_content)
    except TypeError as e:
        print("error reading file "+ fpath_out)
        print(e)
        print("\n\n")
    
    ftxt.close()
