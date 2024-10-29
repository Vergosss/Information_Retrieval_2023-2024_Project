import numpy as np
import pandas as pd
import os
import re
from scipy.stats import rankdata
from matplotlib import pyplot as plt
#vivliothikes
doc_files=[] #ta keimena os stixia listas
#

doc_path = os.getcwd() + "/Collection/docs" #kataskeyi tou monopatiou pou vriskontai ta keimena

#
print(doc_path)#ektyposi aytou tou monopatiou
for file in sorted(os.listdir(doc_path)):#gia kathe string(noumero) ths listas tou path
	file_path = os.path.join(doc_path,file)#ousiastika .../docs/px-1239 kanei join to px ../docs me to 1239 kai vgenei: ../docs/1239
	#print(file_path)
	#print(type(file)) #- einai strings
	#print(int(file))
	if os.path.isfile(file_path):#an to ../docs/1239 px einai arxeio tote:
		f = open(file_path,'r')#anikse to ekastote arxeio se reading mode
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
            inverted_index[word].add(i)#an einai hdh sth lista prosthese to id tou keimenou pou vrisketai h leksi
        else:
            inverted_index[word] = {i}#an den einai sth lista o oros tote prosthese thn emfanisi tou sto keimeno doc
input('WAIT')
		
#-------------------######---------

#pinakas pou krata ton arithmo ton keimenon pou vrisketai mia lexh
Ni = pd.Series(np.zeros(len(words)),index=words)
for word in words:
	Ni[word] = len(inverted_index[word])
	
	
idf = pd.Series(np.zeros(len(words)),index=words)#ypologismos anastrofis syxnotitas emfanisis
for word in words:
	idf[word] = np.log2(len(doc_files)/(Ni[word]))
	#idf[word] = 1 #monadiaio
	#idf[word] = np.log2(1+len(doc_files)/(Ni[word])) -->aplh logarithmiki kanonikopoihsh
	#idf[word] = np.log2(1+(Ni.max())/(Ni[word]))
#print(Ni.head()) #-ok
###------implementation with pandas to test speed------######
tf = pd.DataFrame(np.zeros((len(doc_files), len(words))), columns=words) #mitroo me tis sixnotites emfanisis ton oron ana keimeno
#print(df.head()) #-ok
#print(df.shape) #-ok
#print(df.tail()) #-ok
print('Number of documents where cardiopulmonary exists:',Ni['cardiopulmonary'])

word_split = []
#print(tf['cystic'][1208])
input('WAIT')
for i in range(len(doc_files)):
	word_split = doc_files[i].lower().split()
	for w in list(set(word_split) - set(stop_words)):#ousiastika me ayto gia to sygkekrimeno keimeno asxoloumai mono me tis lekseis tou
	#afou oi ypoloipes lekseis pou den yparxoun sto keimeno exoun fij=0 kai den tha katso na ypologiso - epanalipseis gia mhdenika. glitono
	#ypologistiki isxy-xrono klp
		#tf[w][i] = 1#afou asxoliomaste mono me tis lexeis tou keimenou tha einai anagkastika 1 eno oi ypoloipes 0
		#gegonos pou exoume frontisei arxikopoiontas olo to mitroo se 0
		tf[w][i] = word_split.count(w)#aplh syxnothta emfanisis
		#tf[w][i] = 1 + np.log2(word_split.count(w))#aplh logarithmiki kanonikopoihsh
		#tf[w][i] = 0.5 + 0.5*word_split.count(w)
print('Inverse document frequency of cystic term:',idf['cystic'])
print('Number of documents where cystic exists:',Ni['cystic'])
print('Term frequency i.e number of occurences of cystic term in the last document:',tf['cystic'][1208])
######-----calculating tf-idf-------####

weight = pd.DataFrame(np.zeros((len(doc_files), len(words))), columns=words)#mitroo me ta varh ton oron ana keimeno
for i in range(len(doc_files)):
	word_split = doc_files[i].lower().split()
	for word in list(set(word_split) - set(stop_words)):
		weight[word][i] = tf[word][i] * idf[word]

print(Ni['cf'])
print('Weight of term: cystic, in document 1208(the last document in the collection)',weight['cystic'][1208])
print('Vectors of first 5 documents:',weight.head().iloc[-5:])
#####--------------calculating similarity with test queries-----##
query = "What are the effects of calcium on the physical properties of mucus from CF patients?"
clean_query = re.sub('[^A-Za-z0-9]+', ' ',query)#afairo to erotimatiko kai antikathisto me keno
clean_query = clean_query.lower().strip()#oti keno emeine eksaleifetai
#
print('Cleaning query of extra spaces and special characters:',clean_query)
#
clean_query_split = clean_query.split()
print(clean_query_split)
#
query_weight = pd.Series(np.zeros(len(list(set(clean_query_split)))),index=list(set(clean_query_split)))
#print(query_weight.shape)
frequencies=[]
#vrisko ton oro me th megaliteri syxnothta emfanisis sto erotima
for word in clean_query_split:
	frequencies.append(clean_query_split.count(word))
#print(max(frequencies))
max_freq = max(frequencies)
for word in list(set(clean_query_split)):#calculating wt,q
	if word in words:
		query_weight[word] = (0.5 + 0.5*clean_query_split.count(word)/max_freq)*idf[word]



input('STOP')
query_norm = np.linalg.norm(query_weight)#ypologizo thn l2 norma h alios to metro tou dianysmatos tou erotimatos
doc_norms = np.linalg.norm(weight.values,axis=1)#afou kathe grammh einai ena keimeno ypologizo th norma ton gramon tou
aligned_weight, aligned_query = weight.align(query_weight, axis=1,fill_value=0,broadcast_axis=0)
inner_product = aligned_weight.dot(aligned_query)

#mitroo me ta esoterika ginomena kathe grammhs(keimenou) me to dianysma varon tou query
cosine_similarity = (inner_product)/(query_norm * doc_norms)
#mitroou varon

print('\n10 most matched documents:\n ',cosine_similarity.nlargest(10))
print('\n10 most matched documents:\n ',cosine_similarity.nlargest(10).index)
Ids = cosine_similarity.nlargest(10).index
Ids = np.array(Ids)
print(Ids)
#####

relevant_docs = [721,509,473]#synolo sxetikon me to erotima keimenon
relevant_docs = np.array(relevant_docs)
R = len(relevant_docs) #plithos sxetikon me to query keimenon-synolo R
score = cosine_similarity.nlargest(10).values#pinakas me ta score ton keimenon sto query tha borouse na einai to cosine simularity
score = np.array(score)
sorted_indexes = np.flip(np.argsort(score))#me thn flip pernoume se fthinousa seira ta indeχes tou score: max score-...min score
###
print(sorted_indexes)
#
Ids_sorted = Ids[sorted_indexes]#taxinomimena keimena vash tou score
#sprint(Ids_sorted)
rank = rankdata(score,'max')
ranks = len(rank) - rank + 1
#tha paei me vash to score
print(ranks)

###----pinakas pou deixnei an to i osto keimeno anikei sta sxetika---###
relevant_or_not = np.zeros(len(Ids),dtype=bool)
#
for i in range(len(Ids)):
    if Ids_sorted[i] in relevant_docs:
        relevant_or_not[i] = True
print(relevant_or_not)
#calculating precision and recall#

#
sorted_rank = np.arange(1,len(Ids)+1)#h katataxh kathe keimena
#
Precision = np.zeros(len(Ids))#akriveia gia to query
#
Recall = np.zeros(len(Ids))#anaklisi gia to query
#
for i in range(len(Ids)):
    r = sorted_rank[i]#ousiastika posa keimena exo anaktisei mexri stigmhs
    Precision[i] = sum(relevant_or_not[:r])/r #plithos sxetikon keimenon pou exoun anaktithei eos tora/posa exo anaktisei
    #synolika mexri tora
    Recall[i] = sum(relevant_or_not[:r])/R #plithos sxetikon keimenon pou exo anaktithei mexri stigmis/plithossxetikon me
# to query

#
##------ftiaxno tous synolikous pinakes-#######

table_of_results = pd.DataFrame({'Doc id':Ids,'Score':score,'Rank':ranks})#pinakas me ta apotelesmata tou query to
table_of_metrics = pd.DataFrame({'Rank':sorted_rank,'Doc id':Ids_sorted,'Relevant':relevant_or_not,'Precision':Precision,'Recall':Recall})#

#pinakas ton keimenon taxinomimena vash tou rank tous(vash tou score) mazi me tis times ton precision-recall
print(table_of_results)
print(table_of_metrics)
##----PLOTTING-----##
def Precision_Recall_Graph(precision,recall):
    plt.plot(recall,precision,marker='x',linestyle='--')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision vs Recall')
    plt.grid()
    plt.show()
Precision_Recall_Graph(Precision,Recall)