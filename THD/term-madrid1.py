#!/usr/bin/env file
# -*- coding: utf-8 -*-

import sys 
import csv
import operator
import collections
from operator import itemgetter

def dict_creation(file):
	for line in file.readlines():
		nl = line.split(';',1)
		keyterm = str(nl[0].rstrip())
		data[keyterm] = float(nl[1])
#	print "%s Termhood length = " %file, len(data)
	data2 = score_more_than_1(data)
	return data2

def dict_creation_file2(file):
	for line in file.readlines():
		nl = line.split(';', 1)
		keyterm = str(nl[0].rstrip())
		data[keyterm] = float(nl[1])
	fresult.write("%s:"%len(data))
#	print "%s Termhood length = " %file, len(data)
	data2 = score_more_than_1(data)
	fresult.write("%s: "%len(data2))
	return data2
	
def score_more_than_1(data):
	for keyterm in data:
		if data[keyterm] > 1:
			data2[keyterm] = data[keyterm] 
	data = {}
	data = collections.OrderedDict(sorted(data2.items(), key=itemgetter(1),reverse=True))
#	print data, 'data'
#	print "%s Termhood length - for scores more than 1 = " %file, len(data), "\n"
	return data

def score_more_than_eps(data):
	summa = 0
	eps_s = 0
	score_sum = 0
	data2 = {}
	eps = []
	score_eps = []
	score_sum = sum(data.values())
	score = data.values()
	
	for s in range (0, len(score)-1):
		summa = summa + score[s]
		score_eps.append(summa)
		eps.append(summa/score_sum)
	
	for i in range (0, len(score_eps)-2):
		if eps[i] >= 0.5:
			if score[i+1] <> score[i+2]:
				eps_s = score[i+1]
				break
#	print "eps_s = %s" %eps_s 
		
	for keyterm in data:
		if 	data[keyterm] >= eps_s:
			data2[keyterm] = data[keyterm] 
	
#	print "higher than eps: len(data) = %s" %len(data2)  
# 	fresult.write("sdfgh%s:"%eps_s)
	return data2

def score_more_than_eps_file2(data):
	summa = 0
	eps_s = 0
	score_sum = 0
	data2 = {}
	eps = []
	score_eps = []
	score_sum = sum(data.values())
	score = data.values()
	
	for s in range (0, len(score)-1):
		summa = summa + score[s]
		score_eps.append(summa)
		eps.append(summa/score_sum)
	
	for i in range (0, len(score_eps)-2):
		if eps[i] >= 0.5:
			if score[i+1] <> score[i+2]:
				eps_s = score[i+1]
				break
#	print "eps_s = %s" %eps_s 
		
	for keyterm in data:
		if 	data[keyterm] >= eps_s:
			data2[keyterm] = data[keyterm] 
	
#	print "higher than eps: len(data) = %s" %len(data2)  
	fresult.write("%s: "%len(data2))
	fresult.write("%s: "%eps_s)
	return data2

# Counting thd and thdr

def thd_thdr_first(data, first_file,fresult):
	
	dict_second = data
	max_parser = lambda (d): max([float(a) for a in d.values()])

	def normalize(dictionary,maximum): 
		return {k: float(dictionary[k]) / maximum for k in dictionary}

	dict_second = normalize(dict_second,max_parser(dict_second))

	#thd is sum of normal scores
	thd = sum(dict_second.values()) 
	
	print 'THD of file %s = %s' %(first_file, thd)    

	fresult.write("%s: "%thd)
	thdr = 100
	print 'thdr = ', thdr

	return thdr

def thd_thdr(data1, data2, file1, file2,fresult):
	
	dict_first  = data1
	dict_second = data2

	max_parser = lambda (d): max([float(a) for a in d.values()])

	def normalize(dictionary,maximum): 
		return {k: float(dictionary[k]) / maximum for k in dictionary}

	dict_first = normalize(dict_first,max_parser(dict_first))
	dict_second = normalize(dict_second,max_parser(dict_second))

	sum_norm = sum(dict_second.values())
	print "sum norm = ", sum_norm 

	thd = 0
	thdr = 0

	for key in dict_second:
		try:
			thd = thd + abs(dict_second[key] - dict_first[key])
		except KeyError:
			thd = thd + dict_second[key]

	print 'THD of files %s and %s = %s' %(file1, file2, thd)    

	fresult.write("%s: "%thd)
# Counting thdr = thd/sum_normalized_scores_of_the_second_file * 100

	thdr = thd/sum_norm * 100
	print 'thdr = ', thdr

	return thdr

def printing_results (fresult):
	fresult.write("File_name: ")
	fresult.write("Bag of terms: ")
	fresult.write("More than 1 length: ")
	fresult.write("Terms  in the termhood: ")
	fresult.write("eps: ")
	fresult.write("thd, value: ")
	fresult.write("thdr,%\n")

data = {}
data2= {}
files = []
data_files = []
#-----------------------------------------------------------------------
# Please, write here the list of files you want to work with.
# Each next file in the list is the next iteration (new Termine result)
#-----------------------------------------------------------------------
#'D:\WorkingExample/list_of_files_after_Termine.htm'

infile = 'list.txt'

with open(infile) as f:
    files = f.read().splitlines()

fresult = open('results.csv','w')

printing_results (fresult)	

# Counting data for the very first file

f = open(files[0])
fresult.write("%s: "%files[0])
data = dict_creation_file2(f)

data = score_more_than_eps_file2(data)
thdr_first = thd_thdr_first(data, files[0],fresult)
fresult.write("%s\n"%thdr_first)

for i in range (0, len(files)-1):
	print "------starting new itareation--------"	

# Here are all functions to get data sets. we will proceed to count thd

	data1 = dict_creation(open(files[i]))
	data1 = score_more_than_eps(data1)

	fresult.write("%s: "%files[i+1])
	data2 = dict_creation_file2(open(files[i+1]))
	data2 = score_more_than_eps_file2(data2)

	thdr = thd_thdr(data1, data2, files[i], files[i+1],fresult)
	fresult.write("%s\n"%thdr)

fresult.close()
