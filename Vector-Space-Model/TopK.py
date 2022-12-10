'''
Python 3.0
Retrieve Relevant Documents using Cosine Similarity for
    Exact Retrieval
    Inexact Retrieval through Champion List
    Inexact Retrieval through Cluster Pruning Index
'''
# Add the Relevant File/Folder Paths
stopwords_path = 'Enter The Full Path to Folder with File containing Stop Words'
stopwords_filename = 'File Name of the File with Stop Words (With Extention)'
collection_path = 'Enter The Full Path to Folder with Document Collection'

from collections import defaultdict
from CreateIndex import Create_IndexFn,Query_Vector_Generator,Create_Champion_List,Build_Clusterpruning_Index

# Function to Calculate Cosine Similarity Scores
def TopK_CosineScore(query_vector,k,index):
    scores = defaultdict(lambda: 0)
    for query_term, query_wt in query_vector.items():
        if query_term in index:
            for doc_id, doc_wt, _ in index[query_term][1:]:
                scores[doc_id] += (query_wt * doc_wt)
    TopK_Documents = [X[:2] for X in sorted(scores.items(), key=lambda k: k[1], reverse=True)[:k]]
    return TopK_Documents

def ExactQuerySearch(query,N):
    query_vector = Query_Vector_Generator(query,index)
    ans = TopK_CosineScore(query_vector,N,index)
    return ans

def ChampionListSearch(query,N):
    query_vector = Query_Vector_Generator(query,index)
    ans = TopK_CosineScore(query_vector,N,champion_list)
    return ans

def IndexEliminationSearch(query,N):
    query_terms = query.split()
    newindex = {term : index[term] for term in query_terms}
    newindex = dict(sorted(newindex.items(), key= lambda x: x[1], reverse= True)[:int(len(query_terms)/2)])
    query = ' '.join(newindex.keys())
    query_vector = Query_Vector_Generator(query,newindex)
    ans = TopK_CosineScore(query_vector,N,newindex)
    return ans

def ClusterPruningSearch(query,N):
    query_vector = Query_Vector_Generator(query,clusterpruning_index)
    ans = TopK_CosineScore(query_vector,N,clusterpruning_index)
    return ans

# Create Index 
index = Create_IndexFn(stopwords_path,stopwords_filename,collection_path)

# Create Champion List 
R = 15 # Change this to Required Integer Value
champion_list = Create_Champion_List(index,R)

# Create Cluster Pruning Index
clusterpruning_index = Build_Clusterpruning_Index()

# Retrieve Relevant Documents
query = 'Provide Query As a String Here'
k = 10 # Change this to Required Integer Value
Results_ExactSearch = ExactQuerySearch(query,k)
Results_ChampionList = ChampionListSearch(query,k)
Results_IndexElimination = IndexEliminationSearch(query,k)
Results_ClusterPruning = ClusterPruningSearch(query,k)
