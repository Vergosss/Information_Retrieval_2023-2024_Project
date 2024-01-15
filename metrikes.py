import pandas as pd
import numpy as np
from scipy.stats import rankdata
from matplotlib import pyplot as plt
### arxika exo
Ids = [300,10,100,70,1209,33,44,45]#pinakas me ta ids ton keimenon
Ids = np.array(Ids)#metatropi se array numpy gia na xeiristei meta
relevant_docs = [300,45]#synolo sxetikon me to erotima keimenon
relevant_docs = np.array(relevant_docs)
R = len(relevant_docs) #plithos sxetikon me to query keimenon-synolo R
score = [3,5,1,4,10,20,0,9]#pinakas me ta score ton keimenon sto query tha borouse na einai to cosine simularity
score = np.array(score)
sorted_indexes = np.flip(np.argsort(score))#me thn flip pernoume se fthinousa seira ta indees tou score: max score-...min score
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
