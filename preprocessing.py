import re
import numpy as np
import pandas as pd
import os
import unidecode
doc_files=[] #ta keimena os stixia listas
#
#official_stop_words = set(stopwords.words("english"))
doc_path = os.getcwd() + "/Collection/docs"

#
print(doc_path)
for file in sorted(os.listdir(doc_path)):#gia kathe string(noumero) ths listas tou path
	file_path = os.path.join(doc_path,file)#ousiastika .../docs/px-1239 kanei join to px ../docs me to 1239 kai vgenei: ../docs/1239
	#print(file_path)
	#print(type(file)) #- einai strings
	#print(int(file))
	if os.path.isfile(file_path):#an to ../docs/1239 px einai arxeio tote:
		f = open(file_path,'r')#anikse to ekastote arxeio
		doc_files.append(f.read())#diavase to kai to periexomeno kane to eisagogi sth lista eggrafon

##
docs = []
for i in range(len(doc_files)):
	docs.append(doc_files[i].lower())#metatrepo se mikra grammata olo to keimeno
	docs[i] = docs[i].strip()#afairo an yparxoun kena prin h meta to keimeno(trailing)
	docs[i] = re.sub('[^A-Za-z0-9]+', ' ', docs[i])#afairo tous eidikous xaraktires kai sti thesh tous vazo keno
	docs[i] = re.sub(' +', ' ', docs[i])
	docs[i] = unidecode.unidecode(docs[i])
print(docs[0],len(docs[0].split()))
