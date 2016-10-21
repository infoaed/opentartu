#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/estnltk/pyvabamorf
# pip install pyvabamorf

import re, sys, subprocess, urllib2
from operator import itemgetter
from collections import OrderedDict
from pprint import pprint
    
def dl_doc(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    return response.read()
    
def parse_doc(data):
    doc = {}
    html_title = re.search("(<title>)(.*?)(</title>)", data)
    if html_title:
        doc["html_title"] = html_title.group(2)
    text_title = re.search("(<table.*?>)(.*?)(<table.*?>)", data, re.DOTALL).group(2).split("</font>")
    doc["type_title"] = strip_html(text_title[0]).strip()
    doc["text_title"] = strip_html(text_title[1]).strip()
    header = re.search('(<hr .*?>)(.*?)(<hr .*?>)', data, re.DOTALL).group(2)
    doc["header"] = get_hfields(header)
        
    return doc
    
def strip_html(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
    
def get_hfield(header, name):
    return re.search("<tr.*?>" + name + ".*?</tr>", data)
    
def get_hfields(header):
    data = re.findall("<tr.*?>.*?</tr>", header, re.DOTALL)
    
    fields = {}
    
    for field in data:
        infos = {}
        sep = re.split("</font>.*?</td>", field)
        if len(sep)==1:
            continue
        #print sep
        key = strip_html(sep[0]).strip()
        #print key
        values = sep[1].split("<br>")
        for value in values:
            if len(strip_html(value).strip()) != 0:
                infos["text"] = strip_html(value).strip()
            url = re.findall("href=\".*?\"", value)
            if len(url) > 0:
                infos["url"] = re.search("(\")(.*)(\")", url[0]).group(2)
            #print infos["text"]
            fields[key] = infos
        
    return fields

def scrape_url(url):
    data = dl_doc(url)
    doc = {}
    doc["url"] = url
    full_doc = doc.copy()
    full_doc.update(parse_doc(data))
    
    return full_doc

url = "http://info.raad.tartu.ee/webaktid.nsf/gpunid/G533513B3611D3A1FC2257FE3001F2638?OpenDocument"

if len(sys.argv) >= 2:
	url = sys.argv[1]

#with open("akt.html") as f:
#    data = f.read()

res = scrape_url(url)

pprint(res)
