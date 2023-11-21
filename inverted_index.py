import os #vivliothiki gia diavasma arxeion

doc_files=[] #ta keimena os stixia listas

doc_path = "/home/vergman/Documents/GitHub/Information_Retrieval_2023-2024_Project/Collection/docs/"

for file in os.listdir(doc_path):#gia kathe string(noumero) ths listas tou path
	file_path = os.path.join(doc_path,file)#ousiastika .../docs/px-1239 kanei join to px ../docs me to 1239 kai vgenei: ../docs/1239
	
	if os.path.isfile(file_path):#an to ../docs/1239 px einai arxeio tote:
		f = open(file_path,'r')#anikse to ekastote arxeio
		doc_files.append(f.read())#diavase to kai to periexomeno kane to eisagogi sth lista eggrafon

#print(os.listdir(doc_path))

print('\nNumber of documents in our collection: \n',len(doc_files))#1209 documents
print('\nPrinting the first document: \n',doc_files[0])

tokens =[]#tokens as a list per document

for i in range(len(doc_files)):
	tokens.append(doc_files[i].lower().split())#apo ta keimena pare kathe keimeno ksexorista kai spasto se lekseis. valta os i-osto stixio
	#th lista ayth ton lekseon sta tokens. diladi px. keimeno 5 5-th stixio ton tokens einai h lista me tis lekseis tou keimenou 5

tokens_all = []#all tokens in the collection

for i in range(len(tokens)):
	tokens_all =tokens_all + tokens[i]#enono ola ta tokens se mia eniaia lista
#print(tokens)

print('\nAll tokens in the collection: \n',tokens_all)
terms = list(set(tokens_all))#perno tis monadikes times ton lekseon apo ayth th lista kai etsi exo tous orous to leksilogio mou
print('\nUnique terms gathered from the document collection\n',terms)
print('\nNumber of terms : \n',len(terms))

###
inverted_index = {}

