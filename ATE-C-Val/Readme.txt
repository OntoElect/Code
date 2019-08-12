This folder contains the software for Automated Term Extraction (ATE) using the c-value method. 

Installation via pipenv + pip

For MS Windows, before start you need to install VC compiler for python ( http://aka.ms/vcpython27 )

```
	cd /your/path/to/ATE-C-Val
	pipenv install --python 2.7
	pipenv run python -m pip install nltk numpy pyahocorasick pandas psutil textract
```


Sample call is
cd /your/path/to/ATE-C-Val
pipenv run python python2 ate.py \
  --in_dataset=data/datasets/time/D0000000001.txt \
  --out_terms=data/terms/time/D0000000001.csv \
  --stopwords=data/etc/stopwords.csv \
  --term_patterns=data/etc/term_patterns.csv  \
--min_term_length=3 --min_term_words=2 --trace=0

Parameters are:
--in_dataset=[input TXT file]
--out_terms=[output CSV file containing terms]
--stopwords=[text file containing stopwords, one word per row]
--term_patterns=[text file containing term patterns, one word per row]
--min_term_words=[default=2,number of words in one term]
--min_term_length=[default=3, minimal number of characters in the term]
--trace=1 shows detailed information about execution

Example input files are 
data/datasets/time/D0000000001.txt
data/etc/stopwords.csv
term_patterns.csv
