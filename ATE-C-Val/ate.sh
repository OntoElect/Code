#!/bin/sh
pipenv run python ate.py \
   --in_dataset=data/datasets/time/D0000000001.txt \
   --out_terms=data/terms/time/D0000000001.csv \
   --stopwords=data/etc/stopwords.csv \
   --term_patterns=data/etc/term_patterns.csv  \
   --min_term_length=3 --min_term_words=2 --trace=0

