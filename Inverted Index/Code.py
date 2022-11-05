'''
Python 3.0
Build Inverted Index
Retrieve Relevant Documents for a Query 
'''
import os
import time
from collections import defaultdict

class index:
    def __init__(self,path,fileextention):
        self.path = path
        self.fileextention = '.'+fileextention
        self.inverted_index = None
        self.Corpus = None
        self.docids = None

        
    def buildCorpus(self):
        # Function to Read All Documents from Collection and Create a Corpus
        corpus = []
        docids = {}
        path = self.path
        fileextention = self.fileextention
        i = 0
        # Change Working Directory to Collection Folder
        os.chdir(path)
        # Iterate through All Files in the Collection Folder
        start = time.time()
        for file in os.listdir():
            # Only Add Data from Text Files in the Corpus
            if file.endswith(fileextention):
                file_path = f"{path}/{file}"
                with open(file_path, 'r') as f:
                    # Add Document Data to Corpus
                    corpus.append(f.read().lower())
                    # Store Unique Document Id and Original Document Name
                    docids[i] = file
                    i += 1
        end = time.time()
        print('Corpus Built In : ',end - start,' Seconds.')
        self.Corpus = corpus
        self.docids = docids

        
    def term_pos(self,term,doc):
        # Function (Called by Function 'buildIndex') to return the List of All Indexes of a Term in a Document
        term_pos_lst = []
        for i in range(len(doc)):
            if doc[i]==term:
                term_pos_lst.append(i)
        return term_pos_lst
    

    def buildIndex(self):
        # Function to Build Inverted Index
        corpus = self.Corpus
        inverted_index = defaultdict(list)
        start = time.time()
        # Parsing All Documents from the Corpus
        # Number of Time a Document is Parsed = 1
        for doc in enumerate(corpus):
            # Python List containing Data of Document read in the Iteration
            lst = doc[1].split()
            for term in lst:
                inverted_index[term].append((doc[0],self.term_pos(term,lst)))
        end = time.time()
        print('Index Built In : ',end - start,' Seconds.')
        self.inverted_index = inverted_index
        
        
    def and_query(self,query_terms):
        # Function to Identify Relevant Documents Using the Inverted Index
        inverted_index = self.inverted_index
        docids = self.docids
        start = time.time()
        try:
            # Creating a Dynamic Size List of Sets of Document IDs of Query Terms
            doc_ids = [set() for _ in range(len(query_terms))]
            # Retrieving Document IDs from Inverted Index and Storing them in Dynamic List of Sets
            i = 0
            for query in query_terms:
                for results in inverted_index[query.lower()]:
                    doc_ids[i].add(results[0])
                i += 1
                # Performing AND Operation
            sol = doc_ids[0]
            for ele in doc_ids[1:]:
                sol = sol & ele
            end = time.time()
            # This List Holds Document IDs of All Documents that Satisfy Required Condition
            sol = list(sol)
            print('Results for Query : ',query_terms)
            print('Total Docs Retrieved : ',len(sol))
            for doc in sol:
                print(docids[doc])
        except:
            print('Results for Query : ',query_terms)
            print('Total Docs Retrieved : ',0)
        print('Retrieved In : ',end - start,' Seconds.')

    def print_dict(self):
        # Function to Print the Terms and Posting List in the Inverted Index
        print('Terms and Posting Lists : \n',self.inverted_index)

    def print_doc_list(self):
        # Function to Print Unique Document Id and Original Document Name
        print('Documents and Document Ids : \n',self.docids)
    

path = 'Enter The Full Path to Folder with Document Collection As String Here'
fileextention = 'Enter The File Extention (Eg: TXT) of Document Files'
query = ['Enter','The','Query','as','List','Of','Terms']
obj = index(path,fileextention)
obj.buildCorpus()
obj.buildIndex()
obj.and_query(query)
obj.print_dict()
obj.print_doc_list()
