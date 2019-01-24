#!/usr/bin/env python2
#encoding: UTF-8
import time
import ate4 as ate
import argparse
import re
import csv

import os
import psutil

# reads plain text file
# and generate list of terms

parser = argparse.ArgumentParser()

parser.add_argument("--in_dataset", help="input TXT file")
parser.add_argument("--out_terms", help="output CSV file containing terms")
parser.add_argument("--stopwords", help="text file containing stopwords, one word per row")
parser.add_argument("--term_patterns", help="text file containing term patterns, one word per row")
parser.add_argument("--min_term_words", default=2, help="number of words in one term")
parser.add_argument("--min_term_length", default=3, help="minimal number of characters in the term")
parser.add_argument("--trace", default=0, help="show detailed information about execution")

args = parser.parse_args()

min_term_words=int(args.min_term_words)
min_term_length=int(args.min_term_length)

fp=open(args.stopwords,'r')
stopwords = [r.strip() for r in fp.readlines() if len(r.strip())>0 ]
fp.close()

in_dataset=args.in_dataset
out_terms=args.out_terms

 
trace = ( args.trace=='1' )

print trace

fp=open(args.term_patterns,'r')
term_patterns = [r.strip() for r in fp.readlines() if len(r.strip())>0 ]
fp.close()

print("reading raw TXT from",in_dataset, "writing terms to", out_terms)

t0 = time.time()

fp = open(in_dataset, "r")
doc_txt = fp.read() 
fp.close()
doc_txt = unicode(doc_txt, "utf-8", errors='ignore')
doc_txt = re.sub(r'et +al\.', 'et al', doc_txt)
doc_txt = re.split(r'[\r\n]', doc_txt)


term_extractor = ate.TermExtractor(stopwords=stopwords, term_patterns=term_patterns, min_term_words=min_term_words, min_term_length=min_term_length)
terms = term_extractor.extract_terms(doc_txt, trace=trace)

if trace:
    #print terms[:10]
    print "Term extraction finished"

c_values = term_extractor.c_values(terms, trace=trace) ## replace this line

with open(out_terms, 'wb') as csvfile:
    termwriter = csv.writer(csvfile, delimiter=';', quotechar='', quoting=csv.QUOTE_NONE)
    for cv in c_values:
        termwriter.writerow(cv)


t1 = time.time()
print "finished in ", t1 - t0, " seconds "
process = psutil.Process(os.getpid())
print('used RAM(bytes)=',process.memory_info().rss)  # in bytes 
