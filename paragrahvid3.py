#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re, sys, string
from pyvabamorf import analyze
from pprint import pprint

from urllib.request import urlopen
from urllib.parse import unquote
from urllib.error import URLError

from difflib import SequenceMatcher

import csv, html, codecs

#import collections

IGN_TYYP = ['J', 'Z', 'D', 'P'] # sidesõna, lausemärk, operaator, küsisõna
IGN_WORD = ["olema"]

BF = 25
SLV = 0.8
SLV_YS = 0.95

LAWNAMES = ("seadus", "seadustik")

seadused = {}

def get_para_at(blob, pos):
	willbepara = ""
	for chunk in reversed(latest):
		 if chunk.isnumeric():
			 willbepara = chunk + willbepara
		 else:
			 break
	if len(willbepara)>0:
		return str(int(willbepara))
	return None

def in_dict(nimi):
	highest = 0, None
	for s in seadused.keys():
		seq = SequenceMatcher(None, s, nimi)
		if seq.ratio() > highest[0]:
			highest = seq.ratio(), seadused[s]
	if highest[0] > SLV:
		return highest
	else:
		return 0, None

def lyhike_nimi(cur, add_len):
	for nimi in LAWNAMES:
		if cur.endswith(nimi) and len(cur) <= len(nimi) + add_len:
			return True
	return False
	
def ins_or_add(start, end, data, paras):
	while True:
		lastword = data[start:end].split()[-1]
		#print(lastword)
		if lastword.endswith(LAWNAMES):
			break
		end = end - 1

	chunk=data[start:end]
	if start-BF<0:
		newstart=0
	else:
		newstart=start-BF
	pre=data[newstart:start]
	if end+BF>len(data):
		newend=len(data)
	else:
		newend=end+BF
	post=data[end:newend]

	#print(pre, chunk, post)
	
	closest = 0, None, None
	
	jupid=chunk.split()
	#print(">>>"+" ".join(jupid))
	for i in range(0, len(jupid)):
		variant = jupid[i:len(jupid)]
		cur = " ".join(variant)
		#print(cur)
		if cur in LAWNAMES:
			break
		simil = in_dict(cur)
		if simil[0] > closest[0]:
			#print(i, len(jupid), variant)
			if i == 1 or lyhike_nimi(cur, 4): # viimane sõna, st ühesõnalised seadusenimed
				#print(variant)
				if simil[0] > SLV_YS:
					closest = simil[0], simil[1], cur
					if closest[0] == 1:
						break
			else: # mitmesõnalistega on kõik tavaline
				closest = simil[0], simil[1], cur
				if closest[0] == 1:
					break
	
	if closest[0] > SLV:
		if closest[1] in paras.keys():
			paras[closest[1]] = paras[closest[1]] + 1
		else:
			paras[closest[1]] = 1

		#paras.append(closest)
		#print(closest)

def get_paras(data):
	paras={}
	pat = re.compile(r'[^;.§]+seadus\w*')
	for m in re.finditer(pat, data):
		res = analyze(m.group(0).split()[-1])
		#print(res[0]['analysis'][0])
		if res[0]['analysis'][0]['lemma'].endswith(LAWNAMES):
			ins_or_add(m.start(), m.end(), data, paras)
	return sorted(paras.items(), key=lambda x:x[1], reverse=True)
			
def dl_doc(url):
	while True:
		try:
			resource = urlopen(url)
			content =  resource.read().decode(resource.headers.get_content_charset())	
			break
		except URLError as e:
			print(e)
	return content

def decode_html(data):
	string = unquote(data)
	return html.unescape(string)

def strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_newlines(data):
	return data.replace('\n', ' ').replace('\r', '')   

def get_content(url):
	resp = dl_doc(url)
	content = remove_newlines(strip_html(decode_html(resp)))
	return content

if len(sys.argv) >= 2:
	
	with open("seadused.csv",'r') as csvfile:
		reader = csv.DictReader(csvfile, delimiter='\t', quotechar='"')
		for row in reader:
			seadused[row["nimi"].lower()] = row["lyhend"]

	#print(seadused)
	
	fw = codecs.open("paragrahvid.csv",'w','utf-8')
	
	for arg in sys.argv:
		
		if not arg.endswith(".csv"):
			continue

		with open(arg) as f:
			data_file = f.readlines()

		if arg=="suur_eelnou.csv" or arg=="otsus.csv":
			pos=0
		else:
			pos=1

		for line1 in data_file:
			url = line1.split()[pos].strip('"')
			#url = "http://info.raad.tartu.ee/webaktid.nsf/web/gpunid/GC2257DD200719704C2257CC5001C07BC?OpenDocument"
			#url = "http://info.raad.tartu.ee/webaktid.nsf/web/gpunid/GC2257ED20030C63DC2257E70001D7F80?OpenDocument"
			#url = "http://info.raad.tartu.ee/webaktid.nsf/gpunid/GC2257ED20030C63DC2257C7C00495225"
			#print(url)
			if len(url)>30:
				data = get_content(url)
				#print data
				parad = get_paras(data)
				#print (parad)
				if parad is not None:
					#parad = list(set(parad))
					#print(parad)
					if len(parad)>0:
						tags = []
						for zzz in parad:
							tags.append(zzz[0])
						line = "\""+url+"\"\t\"" + " ".join(tags) + "\""
						print("\""+line.split("/")[-1])
						fw.write(line + "\n")
			sys.exit(1)

	fw.close()

#pprint(words)


