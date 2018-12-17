#!/usr/bin/env python2
#encoding: UTF-8

#
# reads pdf files from directory
# and writes extracted plain text to anoter directory
#

import ate3 as ate
import argparse

from os import listdir
from os.path import isfile, join

parser = argparse.ArgumentParser()

parser.add_argument("--pdfdir", help="input directory containing PDF files")
parser.add_argument("--txtdir", help="output directory containing TXT files")

args = parser.parse_args()

pdfdir=args.pdfdir
txtdir=args.txtdir

print("reading PDF from",pdfdir, "writing txt to", txtdir)




pdf_files=sorted([ (pdfdir, f) for f in listdir(pdfdir) if isfile(join(pdfdir, f)) and f.lower().endswith(".pdf")])
print(pdf_files)

for f in pdf_files:
    fpath_out=join(txtdir, f[1][:-4]+'.txt')
    print(pdfdir,'/',f[1],"=>", fpath_out)
    ftxt = open(fpath_out,'w')
    try:
        #ftxt.write(ate.pdf_to_text_textract(join(f[0], f[1])).replace("\n"," "))
        #file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
        file_content=ate.pdf_to_text_textract(join(f[0], f[1]))
        ftxt.write(file_content)
    except TypeError as e:
        print("error reading file "+ fpath_out)
        print(e)
        print("\n\n")
    
    #file_content=ate.pdf_to_text_textract(join(f[0], f[1]))
    #file_content=ate.pdf_to_text_pypdf(join(f[0], f[1]))
    #ftxt.write(file_content)

    ftxt.close()

print("DONE")