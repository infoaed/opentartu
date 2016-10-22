#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, string
from pyvabamorf import analyze
from pprint import pprint

words={}
table = string.maketrans("","")

IGN_TYYP = ['J', 'Z', 'D', 'P'] # sidesõna, lausemärk, operaator, küsisõna
IGN_WORD = ["olema"]

def ins_or_add(analysis):
	word = analysis['lemma']
	tyyp = analysis['partofspeech']
	#word=word+"_"+tyyp
	if tyyp not in IGN_TYYP and word not in IGN_WORD:
		if word in words.keys():
			words[word] = words[word] + 1
		else:
			words[word] = 1

if len(sys.argv) >= 2:
	with open(sys.argv[1]) as f:
		data = f.readlines()

	for line in data:
		for word in line.split():
			word.translate(table, string.punctuation)
			res = analyze(word)
			ins_or_add(res[0]['analysis'][0])

words = sorted(words.items(), key=lambda x:x[1], reverse=True)

pprint(words)


