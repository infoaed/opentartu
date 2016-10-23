#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, string
from pyvabamorf import analyze
from pprint import pprint

import urllib2, codecs

import collections

IGN_TYYP = ['J', 'Z', 'D', 'P'] # sidesõna, lausemärk, operaator, küsisõna
IGN_WORD = ["olema"]

def get_sum_from_latest(latest):
	willbesum = ""
	for chunk in reversed(latest):
		 if chunk.isnumeric():
			 willbesum = chunk + willbesum
		 else:
			 break
	if len(willbesum)>0:
		return str(int(willbesum))
	return None
	
def ins_or_add(analysis, sums, latest):
	word = analysis['lemma']
	tyyp = analysis['partofspeech']
	#word=word+"_"+tyyp
	if tyyp not in IGN_TYYP and word not in IGN_WORD and word in ("euro"):
		#pprint(latest)
		sss = get_sum_from_latest(latest)
		if sss is not None:
			sums.append(sss)
		
		
def dl_doc(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()

def strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def get_content(url):
	resp = dl_doc(url)
	content = strip_html(resp)
	return content

def get_sums(data):
	sums=[]
	latest=collections.deque(maxlen=5)

	for word in data.split():
		word = word.lower()
		if word in ("eur", "€"):
			print "EUR"
			sss = get_sum_from_latest(latest)
			if sss is not None:
				sums.append(sss)
				latest.append(word)
				continue
		word = filter(unicode.isalnum, unicode(word, "utf-8"))
		#pprint(word)
		if len(word)==0:
			continue
		res = analyze(word)
		ins_or_add(res[0]['analysis'][0], sums, latest)
		latest.append(word)

	return sorted(sums, reverse=True)

if len(sys.argv) >= 2:
	with open(sys.argv[1]) as f:
		data_file = f.readlines()

output=sys.argv[1].split(".")[0]+"-sums.csv"
fw = codecs.open(output,'w','utf-8')

print output

for line1 in data_file:
	url = line1.split()[0].strip('"')
	#print url
	if len(url)>15:
		data = get_content(url)
		#print data
		summad = list(set(get_sums(data)))
		if len(summad)>0:
			line = "\""+url+"\",\"" + " ".join(summad) + "\""
			print line
			fw.write(line + "\n")

fw.close()

#pprint(words)


