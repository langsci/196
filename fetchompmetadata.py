from bs4 import BeautifulSoup
import yaml 
import requests
import sys

bookid = sys.argv[1]
seriesnumber = sys.argv[2]
url = 'http://www.langsci-press.org/catalog/book/%s'%bookid
html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser')

title = soup.find("h1","title").text.strip()
title = title.replace("Forthcoming: ", '')
subtitle = None
try:
  title, subtitle = title.split(': ')
except ValueError:
  pass
author = soup.find("div","langsci_author").text.strip()
try:
  authorfirstname, authorlastname = author.strip().split()
except ValueError:
  authorfirstname, authorlastname = 'UNKNOWN&:','UNKNOWN&:'
blurb = soup.find("div","abstract").div.text.strip()\
	  .replace('\n',' ')\
	  .replace('\r',' ')\
	  .replace(r'\\ ',' ')
authorbio = soup.find("div","author_bios").find("div",'value').text.strip().replace('\n',' ').replace('\r',' ')
series = soup.find("div","series").find("div",'value').text.strip()
#isbns = soup.find("div","publication_format").find_all('div','identification_code')
#isbndict = dict(zip([x.find('div','label').text.strip() for x in isbns],
		    #[x.find('div','value').text.strip() for x in isbns]
		    #))
isbnhc = 1#isbndict["ISBN-13 hardcover (28)"]
isbnsc = 2#isbndict["ISBN-13 softcover (29)"]
bisac = "LAN009000"
if series == "Translation and Multilingual Natural Language Processing": 
    bisac = "LAN023000"
d = {'bookid':bookid,
'title':title,   
'booksubtitle': subtitle,
'series': series,
'seriesnumber': seriesnumber,
'creators' : {
  'authors': [[authorfirstname,authorlastname,authorbio]],
  'editors': None
  },
'blurb': blurb,
'isbns':{ 
  'hardcover':isbnhc,
  'softcover':isbnsc,  
    },
'edition': 1,
'scheme': ["BISAC","LAN009000"],
'colorpages': [-3],
'booklanguage': 'eng'
  }

yamlout=open("metadata.yaml","w")
yaml.dump(d,yamlout,width=10000)
yamlout.close()

seriesd={
"African Language Grammars and Dictionaries":"algad",
"Classics in Linguistics":"classics",
"Contemporary African Linguistics":"calseries",
"Studies in Diversity Linguistics":"sidl",
"Studies in Laboratory Phonology":"silp",
"Language Variation":"lv",
"Translation and Multilingual Natural Language Processing":"tmnlp",
"Morphological Investigations":"mi",
"Empirically Oriented Theoretical Morphology and Syntax":"eotms",
"Topics at the Grammar-Discourse Interface":"tgdi",
"Textbooks in Language Sciences":"tbls" ,
"Open Generative Syntax":"ogs" ,
"Phraseology and Multiword Expressions":"pmwe",
"EuroSLA Studies":"eurosla",
"Niger-Congo Comparative Studies":"nccs"
  }

textemplate=r"""\title{%s}
\BackBody{%s}
\author{%s}
\renewcommand{\lsISBNhardcover}{%s}
\renewcommand{\lsISBNsoftcover}{%s}
\renewcommand{\lsSeries}{%s} 
\renewcommand{\lsSeriesNumber}{%s}
%%\renewcommand{\lsEditorPrefix}{{\LARGE Edited by\\}}
%%\renewcommand{\lsSpineAuthor}{}
%%\renewcommand{\lsSpineTitle}{}
%%\renewcommand{\lsCoverTitleFont}[1]{\sffamily\addfontfeatures{Scale=MatchUppercase}\fontsize{52pt}{16.75mm}\selectfont #1}
%%\subtitle{Change subtitle}
""" 
 
texout=open("localmetadata.tex","w")
texout.write(textemplate%(title,blurb,author,isbnhc,isbnsc,seriesd[series],seriesnumber))
texout.close()
 
 
 

