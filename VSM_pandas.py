import numpy as np
import pandas as pd
import os

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
#
for word in terms:
	if word not in stop_words:
		words.append(word)
######-----INVERTED INDEX-------#####

inverted_index = {}
for i,doc in enumerate(doc_files): #gia kathe keimeno arxika pare to idio to keimeno kai th thesh tou sth lista keimenon
    for word in doc.lower().split():#gia kathe leksi sto ekastote keimeno
        if word in inverted_index:#
            inverted_index[word].add(i+1)#an einai hdh sth lista prosthese to id tou keimenou pou vrisketai h leksi
        else:
            inverted_index[word] = {i+1}#an den einai sth lista o oros tote prosthese thn emfanisi tou sto keimeno doc
input('WAIT')
		
#-------------------######---------
print('Own stopwords list length:',len(stop_words))
print('\nWith stopwords:',len(terms))
print('\nWithout stopwords:',len(words))
#print('English stopwords:',official_stop_words)
#print('English stopwords:',len(official_stop_words))

Ni = pd.Series(np.zeros(len(words)),index=words)
for word in words:
	Ni[word] = len(inverted_index[word])
	
	
idf = pd.Series(np.zeros(len(words)),index=words)
for word in words:
	idf[word] = np.log2(len(doc_files)/Ni[word])
	#exei ki alles parallages
#print(Ni.head()) #-ok
###------implementation with pandas to test speed------######
tf = pd.DataFrame(np.zeros((len(doc_files), len(words))), columns=words)
#print(df.head()) #-ok
#print(df.shape) #-ok
#print(df.tail()) #-ok
print(Ni['cardiopulmonary'])
word_split = []
#print(tf['cystic'][1208])
#print(doc_files[0].lower().split())
input('WAIT')
for i in range(len(doc_files)):
	word_split = doc_files[i].lower().split()
	for w in list(set(word_split) - set(stop_words)):#ousiastika me ayto gia to sygkekrimeno keimeno asxoloumai mono me tis lekseis tou
	#afou oi ypoloipes lekseis pou den yparxoun sto keimeno exoun fij=0 kai den tha katso na ypologiso - epanalipseis gia mhdenika. glitono
	#ypologistiki isxy-xrono klp 
		tf[w][i] = word_split.count(w)
		
print(tf['cystic'][1208])
######-----calculating tf-idf-------####

weight = pd.DataFrame(np.zeros((len(doc_files), len(words))), columns=words)
for i in range(len(doc_files)):
	word_split = doc_files[i].lower().split()
	for word in list(set(word_split) - set(stop_words)):
		weight[word][i] = tf[word][i] * idf[word]
		
