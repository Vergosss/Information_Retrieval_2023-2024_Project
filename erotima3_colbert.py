# -*- coding: utf-8 -*-
"""coIBERT.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fV5BW6KEvByBm4QWGNFAfKZSWyp2e29H

# ColBERTv2: Indexing & Search Notebook

If you're working in Google Colab, we recommend selecting "GPU" as your hardware accelerator in the runtime settings.

First, we'll import the relevant classes. Note that `Indexer` and `Searcher` are the key actors here. Next, we'll download the necessary dependencies.
"""

!git -C ColBERT/ pull || git clone https://github.com/stanford-futuredata/ColBERT.git
import sys; sys.path.insert(0, 'ColBERT/')
import os
from google.colab import drive
drive.mount('/content/drive')

doc_files = []
doc_path = '/content/drive/MyDrive/docs'
for file in sorted(os.listdir(doc_path)):#gia kathe string(noumero) ths listas tou path
	file_path = os.path.join(doc_path,file)#ousiastika .../docs/px-1239 kanei join to px ../docs me to 1239 kai vgenei: ../docs/1239
	#print(file_path)
	#print(type(file)) #- einai strings
	#print(int(file))
	if os.path.isfile(file_path):#an to ../docs/1239 px einai arxeio tote:
		f = open(file_path,'r')#anikse to ekastote arxeio se reading mode
		doc_files.append(f.read())#diavase to kai to periexomeno kane to eisagogi sth lista eggrafon

try: # When on google Colab, let's install all dependencies with pip.
    import google.colab
    !pip install -U pip
    !pip install -e ColBERT/['faiss-gpu','torch']
except Exception:
  import sys; sys.path.insert(0, 'ColBERT/')
  try:
    from colbert import Indexer, Searcher
  except Exception:
    print("If you're running outside Colab, please make sure you install ColBERT in conda following the instructions in our README. You can also install (as above) with pip but it may install slower or less stable faiss or torch dependencies. Conda is recommended.")
    assert False

import colbert

from colbert import Indexer, Searcher
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert.data import Queries, Collection

"""We will use the dev set of the **LoTTE benchmark** we recently introduced in the ColBERTv2 paper. We'll download it from HuggingFace datasets. The dev and test sets contain several domain-specific corpora, and we'll use the smallest dev set corpus, namely lifestyle:dev.

For the purposes of a quick demo, we will only run the `Indexer` on the first 10,000 passages. As we do this, let's also remove the queries whose relevant passages are all outside this small set of passages.
"""

from datasets import load_dataset

dataset = 'lifestyle'
datasplit = 'dev'

collection_dataset = load_dataset("colbertv2/lotte_passages", dataset)
collection = [x['text'] for x in collection_dataset[datasplit + '_collection']]

queries_dataset = load_dataset("colbertv2/lotte", dataset)
queries = [x['query'] for x in queries_dataset['search_' + datasplit]]

f'Loaded {len(queries)} queries and {len(collection):,} passages'









"""This loaded 417 queries and 269k passages. Let's inspect one query and one passage to verify we have done so correctly."""

print(queries[24])
print()
print(collection[19929])
print()

"""## Indexing

For an efficient search, we can pre-compute the ColBERT representation of each passage and index them.

Below, the `Indexer` take a model checkpoint and writes a (compressed) index to disk. We then prepare a `Searcher` for retrieval from this index.
"""

nbits = 2   # encode each dimension with 2 bits
doc_maxlen = 300 # truncate passages at 300 tokens
max_id = 10000

index_name = f'{dataset}.{datasplit}.{nbits}bits'

"""To save space and time, we will only run the `Indexer` on the first 10,000 passages. To do so, we will filter out queries that do not contain passages with ids less than 10,000."""

answer_pids = [x['answers']['answer_pids'] for x in queries_dataset['search_' + datasplit]]
filtered_queries = [q for q, apids in zip(queries, answer_pids) if any(x < max_id for x in apids)]

f'Filtered down to {len(filtered_queries)} queries'

"""Now run the `Indexer` on the collection subset. Assuming the use of only one GPU, this cell should take about six minutes to finish running."""

checkpoint = 'colbert-ir/colbertv2.0'

with Run().context(RunConfig(nranks=1, experiment='notebook')):  # nranks specifies the number of GPUs to use
    config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=nbits, kmeans_niters=4) # kmeans_niters specifies the number of iterations of k-means clustering; 4 is a good and fast default.
                                                                                # Consider larger numbers for small datasets.

    indexer = Indexer(checkpoint=checkpoint, config=config)
    indexer.index(name=index_name, collection=collection[:max_id], overwrite=True)

indexer.get_index() # You can get the absolute path of the index, if needed.

"""## Search

Having built the index and prepared our `searcher`, we can search for individual query strings.

We can use the `queries` set we loaded earlier — or you can supply your own questions. Feel free to get creative! But keep in mind this set of ~300k lifestyle passages can only answer a small, focused set of questions!
"""

# To create the searcher using its relative name (i.e., not a full path), set
# experiment=value_used_for_indexing in the RunConfig.
with Run().context(RunConfig(experiment='notebook')):
    searcher = Searcher(index=index_name, collection=collection)


# If you want to customize the search latency--quality tradeoff, you can also supply a
# config=ColBERTConfig(ncells=.., centroid_score_threshold=.., ndocs=..) argument.
# The default settings with k <= 10 (1, 0.5, 256) gives the fastest search,
# but you can gain more extensive search by setting larger values of k or
# manually specifying more conservative ColBERTConfig settings (e.g. (4, 0.4, 4096)).

query = filtered_queries[13] # try with an in-range query or supply your own
print(f"#> {query}")

# Find the top-3 passages for this query
results = searcher.search(query, k=3)

# Print out the top-k retrieved passages
for passage_id, passage_rank, passage_score in zip(*results):
    print(f"\t [{passage_rank}] \t\t {passage_score:.1f} \t\t {searcher.collection[passage_id]}")