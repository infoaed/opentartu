#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv, sys, io, os, codecs
from StringIO import StringIO

from datetime import datetime
from pytz import timezone

import cgi, cgitb; cgitb.enable()  # for troubleshooting

from pprint import pprint

MAX_INST = 3
TZ = timezone('Europe/Tallinn')

kirjed = {}

kirje_nr = 0

def form_kuup(kuup):
  
  kolm = kuup.split(".")
  
  if len(kolm) != 3:
      return kuup
      
  if int(kolm[1])==1:
    kolm[1] = "jaan"
  elif int(kolm[1])==2:
    kolm[1] = "veebr"
  elif int(kolm[1])==3:
    kolm[1] = "märts"
  elif int(kolm[1])==4:
    kolm[1] = "aprill"
  elif int(kolm[1])==5:
    kolm[1] = "mai"
  elif int(kolm[1])==6:
    kolm[1] = "juuni"
  elif int(kolm[1])==7:
    kolm[1] = "juuli"
  elif int(kolm[1])==8:
    kolm[1] = "aug"
  elif int(kolm[1])==9:
    kolm[1] = "sept"
  elif int(kolm[1])==10:
    kolm[1] = "okt"
  elif int(kolm[1])==11:
    kolm[1] = "nov"
  elif int(kolm[1])==12:
    kolm[1] = "dets"
    
  reaalne = kolm[0]+ ".<br>" + kolm[1] + "<br>" + kolm[2]

  
  return reaalne

def gene_tempel(kuup, kell):
  kolm = kuup.split(".")
  if kell != "":
    kaks = kell.split(" - ")[0].split(":")
  else:
    kaks = [23, 59] # enne keskööd

  #print kaks
  
  if len(kolm) != 3:
      return None # date(2016, 1, 1)
  
  return datetime(int(kolm[2]), int(kolm[1]), int(kolm[0]), int(kaks[0]), int(kaks[1]))


def get_tags(url):
  report_itself = io.open("tags.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')

  # url

  for row in refs:
    if row[0] == url:
       return row[1].split(" ")
       
  return []

def get_sums(url):
  report_itself = io.open("sums.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')

  for row in refs:
    if row[0] == url:
       return row[1].split(" ")
       
  return []

def get_paras(url):
  report_itself = io.open("paragrahvid.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')

  for row in refs:
    if row[0] == url:
       return row[1].split(" ")
       
  return []

def lisa_kirje(pealkiri, tegija, peaurl, tekst = "", nimed = [], kuup = "", kell = "", tagid = [], summad = [], paras = []):
  ajatempel = gene_tempel(kuup, kell)
  vahe = peaurl.split("/")[-1]
  l6pp = vahe.rpartition("?")
  if len(l6pp[0]) == 0:
    identiteet = vahe
  else:
    identiteet = l6pp[0]
  
  if ajatempel is not None:
    if kirjed.get("identiteet") is not None:
      print "totaalne jama"
      return None
    kirjed[identiteet] = {
      "pealkiri": pealkiri,
      "tegija": tegija,
      "url": peaurl,
      "tekst": tekst,
      "nimed": nimed,
      "kuup": kuup,
      "kell": kell,
      "aeg": ajatempel,
      "sildid": tagid,
      "summad": summad,
      "seadus": paras
    }
  else:
    print "jama"
    return None
    
  return kirjed[identiteet]
 
def kirje(pealkiri, tegija, peaurl, tekst = "", nimed = [], kuup = "", tagid = [], summad = [], paras = []):
  global kirje_nr

  print '<div class="panel kirje">'
  if kirje_nr > 0: print '<i class="fa fa-long-arrow-down"></i>'
  print '<div class="panel-heading" role="button" data-toggle="collapse" href="#clp%d" aria-expanded="false" aria-controls="clp%d">' % (kirje_nr, kirje_nr)
  print '<h4 class="list-item">%s %s<span class="label label-info kuupaev">%s</span>' % (tegija, tekst, form_kuup(kuup))
  for nimi in nimed:
    print '<span class="badge nimi">%s</span>' % (nimi)
  for tggg in tagid:
    print '<span class="badge tag">#%s</span>' % (tggg)
  for summa in summad:
    print '<span class="badge raha">€%s</span>' % (summa)
  for para in paras:
    print '<span class="badge seadus">%s</span>' % (para)
  print '</h4><p>%s</p>' % (pealkiri)
  print '</div>'
  print '<div class="collapse panel-body" id="clp%d">' % (kirje_nr)
  print '<a href="%s">%s</a>' % (peaurl, pealkiri)
  print '</div>'
  print '</div>'
  
  kirje_nr = kirje_nr + 1




def get_lv_eelnou(url):
  report_itself = io.open("vaike_eelnou.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')

  for row in refs:
    if row[0] == url:
       return row
       
  return None
       

def get_lv_istung(url):
  report_itself = io.open("istungiProtokollid.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')

  for row in refs:
    if row[0] == url:
       return row
       
  return None
    

#suure eelnõu url
def get_protod(url): 
  report_itself = io.open("koosolekuProtokollid.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')
  
  protod = []
    
  for row in refs:
    if row[0] == url:
       protod.append(row)

  
  return protod

def get_suur(url):
  report_itself = io.open("suur_eelnou.csv", "rt", encoding="UTF-8", errors="replace").read()
  source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
  refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')
  
  for row in refs:
    if row[0] == url:

      return row

  return None
  

# html queries
form = cgi.FieldStorage()
print "Content-Type: text/html"
print
print """
<!DOCTYPE html>
<html lang="et">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

  <!-- Latest compiled and minified CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

  <!-- Optional theme -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
  
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.6.1/css/font-awesome.min.css">

  <style>
  .kirje {
    margin-bottom: 0;
    border-bottom:1px solid #ccc;
    position: relative;
  }
  .kirje.minevik{
    color:#ccc;
  }
  .kirje i.fa-long-arrow-down{
    font-size:2em;
    position: absolute;
    right:7em;
    top:-0.45em;
    color:#ccc;
  }
  .aktuaalne {
    background-color: lightblue;
  }

  .kuupaev {
    float: left;
    padding: 0.3em 0.5em 0.3em 0.5em;
    margin-right: 1em;
    display: visible;
  }
  .tag {
    float: right;
    background-color: darkgreen;
    display: visible;
  }    
  .nimi {
    float: right;
    background-color: navy;
    display: visible;
  }
  .raha {
    float: right;
    background-color: darkorange;
    display: visible;
  }
  .seadus {
    float: right;
    background-color: purple;
    display: visible;
  }
  </style>



  <title>Open Tartu (for Smart Citizens)</title>

  <!-- Bootstrap -->


  <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      <![endif]-->
    </head>
    <body>


      <!-- Modal -->
      <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <h4 class="modal-title" id="myModalLabel">Siia tulevad isiku detailid</h4>
            </div>
            <div class="modal-body">
              <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Urmas_klaas_hansap%C3%A4eval.jpg/220px-Urmas_klaas_hansap%C3%A4eval.jpg">
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>

        <label style="float: left; text-shadow: 0 -1px 0 rgba(0,0,0,.2); font-size: 24px; background-color: #265a88; border-color: #245580; background-color: #265a88;
border-color: #245580; font-weight: 1000; color: white;">
          &nbsp; <a href="http://infoaed.github.io/start.html" style="text-decoration: none; color: white;">#openTartu</a> &nbsp; 
        </label>
      <div class="btn-group" data-toggle="buttons">
        <label class="btn btn-primary active">
          <input id="kuupaev_cb" type="checkbox" autocomplete="off" checked>Kuupäev
        </label>
        <label class="btn btn-primary active">
          <input id="nimi_cb" type="checkbox" autocomplete="off" checked>Isik
        </label>
        <label class="btn btn-primary active">
          <input id="tag_cb" type="checkbox" autocomplete="off" checked>Silt
        </label>
        <label class="btn btn-primary active">
          <input id="raha_cb" type="checkbox" autocomplete="off" checked>Raha
        </label>
        <label class="btn btn-primary active">
          <input id="seadus_cb" type="checkbox" autocomplete="off" checked>Seadus
        </label>
      </div>

"""

otsus_id = ""

try:
  otsus_id = form["id"].value
except KeyError:
  pass

report_itself = io.open("otsus.csv", "rt", encoding="UTF-8", errors="replace").read()
source = report_itself.encode("utf-8").lstrip(codecs.BOM_UTF8)
refs = csv.reader(StringIO(source), delimiter="\t", quotechar='"')

peaurl = "http://info.raad.tartu.ee/webaktid.nsf/web/viited/"+otsus_id

for row in refs:
  if row[0] == "http://info.raad.tartu.ee/webaktid.nsf/web/viited/"+otsus_id:
     suur = row[11]
     protod = []
     
     suureel = get_suur(suur)
     protod = get_protod(suur)
     lv_eeln = get_lv_eelnou(suur)
     istung = get_lv_istung(suur)

     #for proto in protod:

     if lv_eeln is not None:
       lisa_kirje(lv_eeln[7], lv_eeln[5], lv_eeln[1], tekst = "eelnõu", nimed = [ lv_eeln[9], lv_eeln[11] ], kuup=lv_eeln[10], summad=get_sums(lv_eeln[1])[0:MAX_INST], tagid=get_tags(lv_eeln[1])[0:MAX_INST], paras=get_paras(lv_eeln[1]))
       #kirje(lv_eeln[7], lv_eeln[5], lv_eeln[1], tekst = "eelnõu", nimed = [ lv_eeln[9], lv_eeln[11] ], kuup=lv_eeln[10], summad=get_sums(lv_eeln[1])[0:MAX_INST], tagid=get_tags(lv_eeln[1])[0:MAX_INST], paras=get_paras(lv_eeln[1]))
     if istung is not None:
       lisa_kirje(istung[7], istung[4], istung[1], tekst = "istung", nimed = [ istung[9], istung[10] ], kuup=istung[5], kell=istung[8], summad=get_sums(istung[1])[0:MAX_INST], tagid=get_tags(istung[1])[0:MAX_INST], paras=get_paras(istung[1]))
       #kirje(istung[7], istung[4], istung[1], tekst = "istung", nimed = [ istung[9], istung[10] ], kuup=istung[5], summad=get_sums(istung[1])[0:MAX_INST], tagid=get_tags(istung[1])[0:MAX_INST], paras=get_paras(istung[1]))
     for proto in protod:
       lisa_kirje(proto[8], proto[5], proto[1], nimed =[ proto[12], proto[13] ], kuup=proto[9], kell=proto[10], summad=get_sums(proto[1][0:MAX_INST]), tagid=get_tags(proto[1])[0:MAX_INST], paras=get_paras(proto[1]))
       #kirje(proto[8], proto[5], proto[1], nimed =[ proto[12], proto[13] ], kuup=proto[9], summad=get_sums(proto[1][0:MAX_INST]), tagid=get_tags(proto[1])[0:MAX_INST], paras=get_paras(proto[1]))
     juhtkomisjon = suureel[12]
     lisa_kirje(suureel[6], suureel[4], suur, tekst="eelnõu", nimed = [suureel[8], suureel[10]], kuup=suureel[9], summad=get_sums(suureel[0])[0:MAX_INST], tagid=get_tags(suureel[0])[0:MAX_INST], paras=get_paras(suureel[0]))
     #kirje(suureel[6], suureel[4], suur, tekst="eelnõu", nimed = [suureel[8], suureel[10]], kuup=suureel[9], summad=get_sums(suureel[0])[0:MAX_INST], tagid=get_tags(suureel[0])[0:MAX_INST], paras=get_paras(suureel[0]))
     lisa_kirje(row[5], row[3], peaurl, "otsus", kuup=row[8], summad=get_sums(row[0])[0:MAX_INST], tagid=get_tags(row[0])[0:MAX_INST], paras=get_paras(row[0]))
     #kirje(row[5], row[3], peaurl, "otsus", kuup=row[8], summad=get_sums(row[0])[0:MAX_INST], tagid=get_tags(row[0])[0:MAX_INST], paras=get_paras(row[0]))

     kirjed_jrk = sorted(kirjed.items(), key=lambda x:x[1], reverse=False)
     
     #print "<pre>"
     for krj in kirjed_jrk:
       x = krj[1]
       #pprint(x)
       kirje(pealkiri=x["pealkiri"], tegija=x["tegija"], peaurl=x["url"], tekst=x["tekst"], nimed=x["nimed"], kuup=x["kuup"], tagid=x["sildid"], summad=x["summad"], paras=x["seadus"])

     #print "<pre>"
     #pprint(kirjed_jrk)
     #print "</pre>"

print """
      <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
      <!-- Include all compiled plugins (below), or include individual files as needed -->

      <!-- Latest compiled and minified JavaScript -->
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>



  <script>
  $("#tag_cb").change(function() {
      if(this.checked) {
        $(".tag").each(function( index ) {
          $( this ).show();
        });
      } else {
        $(".tag").each(function( index ) {
          $( this ).hide();
        });
      }
  });

  $("#nimi_cb").change(function() {
      if(this.checked) {
        $(".nimi").each(function( index ) {
          $( this ).show();
        });
      } else {
        $(".nimi").each(function( index ) {
          $( this ).hide();
        });
      }
  });

  $("#raha_cb").change(function() {
      if(this.checked) {
        $(".raha").each(function( index ) {
          $( this ).show();
        });
      } else {
        $(".raha").each(function( index ) {
          $( this ).hide();
        });
      }
  });

  $("#seadus_cb").change(function() {
      if(this.checked) {
        $(".seadus").each(function( index ) {
          $( this ).show();
        });
      } else {
        $(".seadus").each(function( index ) {
          $( this ).hide();
        });
      }
  });

  $("#kuupaev_cb").change(function() {
      if(this.checked) {
        $(".kuupaev").each(function( index ) {
          $( this ).show();
        });
      } else {
        $(".kuupaev").each(function( index ) {
          $( this ).hide();
        });
      }
  });

  $(".nimi").click(function(e){
    e.stopPropagation();
    $("#myModal").modal('show');
  })
    </script>

<script id="dsq-count-scr" src="//open-tartu-for-smart-citizens.disqus.com/count.js" async></script>

<div id="disqus_thread"></div>
<script>

/**
*  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
*  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/

var disqus_config = function () {
"""
print 'this.page.url = "http://tartuvabakond.dorpatensis.ee/index.py?id=%s";' % (otsus_id)
print 'this.page.identifier = "%s";' % (otsus_id)
print """
};

(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = '//open-tartu-for-smart-citizens.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
                                

</body>
</html>




"""


