import os #vivliothiki gia diavasma arxeion
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
doc_files=[] #ta keimena os stixia listas
#
official_stop_words = set(stopwords.words("english"))
doc_path = os.getcwd() + "\Collections\docs"

print(doc_path)
for file in sorted(os.listdir(doc_path)):  # gia kathe string(noumero) ths listas tou path
    file_path = os.path.join(doc_path,file)  # ousiastika .../docs/px-1239 kanei join to px ../docs me to 1239 kai vgenei: ../docs/1239
    #print(file_path)
    if os.path.isfile(file_path):  # an to ../docs/1239 px einai arxeio tote:
        f = open(file_path, 'r')  # anikse to ekastote arxeio
        doc_files.append(f.read())  # diavase to kai to periexomeno kane to eisagogi sth lista eggrafon

# print(os.listdir(doc_path))
print('\nNumber of documents in our collection: \n', len(doc_files))  # 1209 documents
#print('\nPrinting the first document: \n', doc_files[0])

#input('.........')

tokens = []  # tokens as a list per document

for i in range(len(doc_files)):
    tokens.append(doc_files[i].lower().split())  # apo ta keimena pare kathe keimeno ksexorista kai spasto se lekseis. valta os i-osto stixio
# th lista ayth ton lekseon sta tokens. diladi px. keimeno 5 5-th stixio ton tokens einai h lista me tis lekseis tou keimenou 5

tokens_all = []  # all tokens in the collection

for i in range(len(tokens)):
    tokens_all = tokens_all + tokens[i]  # enono ola ta tokens se mia eniaia lista
# print(tokens)

print('\nAll tokens in the collection: \n', tokens_all)
terms = list(set(tokens_all))  # perno tis monadikes times ton lekseon apo ayth th lista kai etsi exo tous orous to leksilogio mou
print('\nUnique terms gathered from the document collection\n', terms)
print('\nNumber of terms : \n', len(terms))

##
words = []
stop_words = ["a", "an", "the", "and", "but", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", "just"]
#
for word in terms:
	if word not in stop_words:
		words.append(word)
print(len(stop_words))
print('\nWith stopwords:',len(terms))
print('\nWithout stopwords:',len(words))
print('English stopwords:',official_stop_words)
print('English stopwords:',len(official_stop_words))
#
inverted_index = {}
for i,doc in enumerate(doc_files): #gia kathe keimeno arxika pare to idio to keimeno kai th thesh tou sth lista keimenon
    for word in doc.split():#gia kathe leksi sto ekastote keimeno
        if word in inverted_index:#
            inverted_index[word].add(i)#an einai hdh sth lista prosthese to id tou keimenou pou vrisketai h leksi
        else:
            inverted_index[word] = {i}#an den einai sth lista o oros tote prosthese thn emfanisi tou sto keimeno doc
print(inverted_index)
###
#-----STO VECTOR SPACE MODELO document(w1,w2,w3,.....,wn)- kathe keimeno einai ena dianysma varon
#synartisi metatropis keimenon se dianysmata
#An valo binary=True ----> tf={0,1]
#an valo use_idf = True/false me false tote idf=1
#an valo sublinear_tf =True tote tf=1+log(tf)



##
tfidf_vectorizer = TfidfVectorizer(binary=True,use_idf=False)# an valo false idf=1
tfidf_matrix = tfidf_vectorizer.fit_transform(doc_files)#ypologizo to mitroo Tf-idf to varos diladi kathe orou sta keimena
#ksekinaei eggrafo1 (proto stixio tou array) kathe lexh-poses fores emfanizetai sto eggrafo
#meta eggrafo2(deytero stixio tu array) kathe lexh-poses fores emfanizetai k.o.k
print('---------------Tf-idf matrix(non matrix):\n',tfidf_matrix)#
print('---------------Tf-idf matrix:\n',tfidf_matrix.toarray())
###synartisi metrisis syxnotiton
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(doc_files)
print('---------------Words in collection:\n',vectorizer.get_feature_names_out())#oles oi lexeis
#ftiaxnei to mitroo syxnotiton emfanisis kathe lexis sto lexiko:
#ksekinaei eggrafo1 (proto stixio tou array) kathe lexh-poses fores emfanizetai sto eggrafo
#meta eggrafo2(deytero stixio tu array) kathe lexh-poses fores emfanizetai k.o.k
#to mhden-0 deixnei oti h leksh den yparxei sto eggrafo. gia na yparxei omoiomorfia
print('---------------List size(number of words):\n',len(vectorizer.get_feature_names_out()))
print(X.toarray())#metatrepei thn pano pliroforia se array
