'''
Python 3.0
Retrieve Relevant Documents for a Query using Boolean Retrieval Model
'''

import nltk
from InvertedIndex import Inverted_Index_Fn

def BooleanRetrievelModel(inverted_index,query_terms,booloperand):
    try:
        # Creating a List of Sets that will hold Document Names of Documents Relevant to Query Terms
        doc_ids = [set() for _ in range(len(query_terms))]
        # Retrieving Document Names from Inverted Index and Storing them in Sets created Above
        i = 0
        for term in query_terms:
            doclist = inverted_index[term.lower()]
            doc_ids[i].add(doclist)
            i += 1
        # Performing Boolean Operation on Relevant Set of Documents
        sol = doc_ids[0]
        for ele in doc_ids[1:]:
            if booloperand=='AND':
                sol = sol & ele
            elif booloperand=='OR':
                sol = sol | ele
        # This List Holds Document Names of All Relevant Documents for the Given Query
        relevant_documents_list = list(sol)
    except:
        relevant_documents_list = []
    return relevant_documents_list

'''
    Pre-Process Query
        - Remove All Punctuations
        - Convert to Lower Case
'''
def PreProcessQuery(query):
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    query = ' '.join(tokenizer.tokenize(query))
    query = query.lower().split()
    return query


# Add the Relevant File/Folder Paths
stopwords_path = 'Enter The Full Path to Folder with File containing Stop Words'
stopwords_filename = 'File Name of the File with Stop Words (With Extention)'
collection_path = 'Enter The Full Path to Folder with Document Collection'

# Create Inverted Index 
inverted_index = Inverted_Index_Fn(stopwords_path,stopwords_filename,collection_path)

# Choose booloperand='AND' or booloperand='OR' as desired
booloperand = ''

# Pre-Processing the String
query = 'Provide Query As a String Here'
query = PreProcessQuery(query)

# The Following List Contains All Documents Relevant to Query Retrieved through Boolean Retrieval Model
relevant_docs = BooleanRetrievelModel(inverted_index,query,booloperand)

