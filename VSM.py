import os #vivliothiki gia diavasma arxeion
#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
#from nltk import wordpunct_tokenize
#from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
print('\nNumber of documents in our collection: \n',len(doc_files))#1209 documents
#print('\nPrinting the first document: \n',doc_files[0])
input('Waiting...')
tokens =[]#tokens as a list per document

for i in range(len(doc_files)):
	tokens.append(doc_files[i].lower().split())#apo ta keimena pare kathe keimeno ksexorista kai spasto se lekseis. valta os i-osto stixio
	#th lista ayth ton lekseon sta tokens. diladi px. keimeno 5 5-th stixio ton tokens einai h lista me tis lekseis tou keimenou 5

tokens_all = []#all tokens in the collection

for i in range(len(tokens)):
	tokens_all = tokens_all + tokens[i]#enono ola ta tokens se mia eniaia lista
#print(tokens)

#print('\nAll tokens in the collection: \n',tokens_all)
terms = list(set(tokens_all))#perno tis monadikes times ton lekseon apo ayth th lista kai etsi exo tous orous to leksilogio mou
#print('\nUnique terms gathered from the document collection\n',terms)
print('\nNumber of terms : \n',len(terms))

###

#
words = []
stop_words = ["a", "an", "the", "and", "but", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just"]
#--- removing stop words---#
for word in terms:
	if word not in stop_words:
		words.append(word)
#
print('Own stopwords list length:',len(stop_words))
print('\nWith stopwords:',len(terms))
print('\nWithout stopwords:',len(words))
#print('English stopwords:',official_stop_words)
#print('English stopwords:',len(official_stop_words))
#---creating the inverted index----#
inverted_index = {}
for i,doc in enumerate(doc_files): #gia kathe keimeno arxika pare to idio to keimeno kai th thesh tou sth lista keimenon
    for word in doc.lower().split():#gia kathe leksi sto ekastote keimeno
        if word in inverted_index:#
            inverted_index[word].add(i+1)#an einai hdh sth lista prosthese to id tou keimenou pou vrisketai h leksi
        else:
            inverted_index[word] = {i+1}#an den einai sth lista o oros tote prosthese thn emfanisi tou sto keimeno doc

#for i,doc in enumerate(doc_files):
	#print(i,doc)
print(inverted_index['cystic'])
#print(doc_files[824])
#
print(len(inverted_index['cystic']))

input('WAIT')
Ni ={}
#
for word in words:
	Ni[word] = 0
#
#
for word in words:
	Ni[word] = len(inverted_index[word])
	
	
	
#calculating frequency of each word in the collection(in how many documents it exists)
'''
for word in words:#ta words einai mikra
	for doc in doc_files:
		if word in doc.lower().split():
			Ni[word] = Ni.get(word) + 1
'''
#
#print(Ni)
print(Ni['cystic'])
#
idf = {}
#

for word in words:
	idf[word] = np.log2(len(doc_files)/Ni[word])#idf=log(N/Ni)
	#idf[word] = np.log2(1 + len(doc_files)/Ni[word])
	#idf[word] = 1
print(idf['cystic'])
#print(idf)
###---calculating tf for each document--------##

tf = {} # term frequence for each term for each document
#sthn ousia ftiaxno ena nested dictionary


print(doc_files[1208])

input('WAIT')
for i,doc in enumerate(doc_files):
	tf[i+1] = {} #initialization

for word in words:
	for i,doc in enumerate(doc_files):
		tf[i+1][word] = doc.lower().split().count(word)
		
print(tf[1209]['cystic'])

input('WAIT AGAIN')
#### now calculating the weight for each word in each document wij=tfij * idfi
weight = {}
#initialization
for i,doc in enumerate(doc_files):
	weight[i+1] = {}
	
#
for word in words:
	for i,doc in enumerate(doc_files):
		weight[i+1][word] = tf[i+1][word] * idf[word] #vector space model definition
	
	
	
