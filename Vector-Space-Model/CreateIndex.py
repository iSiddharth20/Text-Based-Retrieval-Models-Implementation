'''
Python 3.0
Create Required Index, Champion List, Cluster Pruning Index
'''

# Importing Necessary Libraries
import os
import nltk
import math
import random
from collections import Counter
from collections import defaultdict

# Tokenizer to keep only Alpha-Numeric Terms  [a-zA-Z0-9_]
tokenizer = nltk.RegexpTokenizer(r"\w+")

'''
    Corpus will be Stored as Dictionary of Format :
    {
        DocId1 : ['Entire','Document','As','Pre-Processed','Tokenized','List'....]
        DocId2 : ['Entire','Document','As','Pre-Processed','Tokenized','List'....]
        .
        .
        .
    }
'''
global corpus
corpus = {}
'''
    Index will be Stored as a Dictionary of Format :
    { 
        term1 : [ idf_term1, [DocId1,tf_DocId1,[index1,index2,...]] , [DocId2,tf_DocId2,[index1,index2,...]] , ... ]
        term2 : [ idf_term2, [DocId1,tf_DocId1,[index1,index2,...]] , [DocId2,tf_DocId2,[index1,index2,...]] , ... ]
        .
        .
        .
    }
'''
global index
index = defaultdict(list)

'''
Pre-Process Document Data
     - Remove All Punctuations
     - Convert to Lower Case
'''
def PreProcess(data):
    data = ' '.join(tokenizer.tokenize(data))
    data = data.lower()
    return data

# Function to Calculate Freequency of All Terms in Entire Corpus
def term_freq_corpus(corpus):
    term_freq_c = Counter({})
    for doc in corpus:
        term_freq_c += Counter(corpus[doc])
    return term_freq_c
    
# Function to Calculate TF,IDF Values of a Term
def tfidf_val_calc(term,term_indxs_lst,ln_corpus,term_freq_c):
    # tf : Term Freequency of Term in Document, rounded off to 8 decimal places
    try:
        tf = round(((1 + math.log10(len(term_indxs_lst[term])))),8)
    except:
        tf = 0
    # idf : Inverse Document Freequency of Term in Corpus, rounded off to 8 decimal places
    try:
        idf = round((math.log10(ln_corpus / term_freq_c[term])),8)
    except:
        idf = 0
    return tf,idf

# Function to Calculate Query Vector
def Query_Vector_Generator(query,index):
    query = PreProcess(query)
    query = query.split()
    query_vector = defaultdict(lambda: 0)
    for term in query:
        try:
            query_vector[term] = index[term][0]
        except:
            query_vector[term] = 0
    return query_vector

def Create_IndexFn(stopwords_path,stopwords_filename,collection_path):
    # Getting StopWords from a File (Optional)
    '''
    For Windows Users, Use the following line of code to open file  
        with open(path+'\'+filename) as f:
    '''
    with open(stopwords_path+'/'+stopwords_filename) as f:
        global stopwords
        stopwords = f.read().split('\n')
        
    # Changing Working Directory to the Folder that contains Document Collection 
    os.chdir(collection_path)

    '''
    Reading, Pre-Processing Document Collection and Creating Corpus
    It is assumed that Document Collection is in '.txt' files

    For Windows Users, Use the following line of code to open file  
        file_path = f".\{file}"
    '''
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"./{file}"
            with open(file_path, "r") as f:
                doc_data = f.read()
            doc_data = PreProcess(doc_data)
            corpus[file[:-4]] = doc_data.split() # [:-4] to Remove '.txt' from FileName which will be used as DocId
    
    global ln_corpus 
    ln_corpus = len(corpus)
    
    term_freq_c = term_freq_corpus(corpus)
    
    # Create Required Index
    for docId in corpus:
        # term_indxs_lst Stores All Indexes Of a Term in a Document
        term_indxs_lst = defaultdict(list) 
        doc_data = corpus[docId]
        # Such Method Avoids Indexing of Same Term for the Same Document
        for i,term in enumerate(doc_data):
            if term not in stopwords:
                # By Convention, Indexing of Terms in a Document Starts at 1
                term_indxs_lst[term].append(i+1)
        for term in term_indxs_lst:
            # Calculate TF,IDF Values for the Term
            tf , idf = tfidf_val_calc(term,term_indxs_lst,ln_corpus,term_freq_c)
            # Weight = TF-IDF Value of the Term for the Particular Document
            wt = round((tf*idf),8)
            if len(index[term]) == 0:
                index[term].append(idf)
            index[term].append([docId, wt, term_indxs_lst[term]])
    # Return the Index
    return index

# Create a Champion List
def Create_Champion_List(index,R):
    champion_list = defaultdict(list)
    for term in index:
        # Sorts on the Basis of Term Weight in the Document
        lst = sorted(index[term][1:], key=lambda k: k[1], reverse=True)[:R]
        champion_list[term] = lst
    return champion_list

# Create Cluster Pruning Index
def Build_Clusterpruning_Index():
    clusterpruning_index = defaultdict(list)
    docs = corpus.keys()
    leaders_no = math.ceil(math.sqrt(len(docs)))
    leaders = set(random.sample(list(docs), leaders_no))
    new_corpus = {docid: corpus[docid] for docid in leaders}
    ln_corpus = len(new_corpus)
    term_freq_nc = Counter({})
    for doc in new_corpus:
        term_freq_nc += Counter(new_corpus[doc])
    for docId in new_corpus:
        term_indxs_lst = defaultdict(list) 
        doc_data = new_corpus[docId]
        for i,term in enumerate(doc_data):
            if term not in stopwords:
                term_indxs_lst[term].append(i+1)
        for term in term_indxs_lst:
            tf , idf = tfidf_val_calc(term,term_indxs_lst,ln_corpus,term_freq_nc)
            wt = round((tf*idf),8)
            if len(clusterpruning_index[term]) == 0:
                clusterpruning_index[term].append(idf)
            clusterpruning_index[term].append([docId, wt, term_indxs_lst[term]])
    return clusterpruning_index
