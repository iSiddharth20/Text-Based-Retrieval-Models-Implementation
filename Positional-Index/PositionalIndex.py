'''
Python 3.0
Build Positional Index
'''
# Importing Necessary Libraries
import os
import nltk

def Positional_IndexFn(stopwords_path,stopwords_filename,collection_path):
    # Getting StopWords from a File (Optional)
    '''
    For Windows Users, Use the following line of code to open file  
        with open(path+'\'+filename) as f:
    '''
    with open(stopwords_path+'/'+stopwords_filename) as f:
        stopwords = f.read().split('\n')
        
    #Changing Working Directory to the Folder that contains Document Collection 
    os.chdir(collection_path)

    # Tokenizer to keep only Alpha-Numeric Words  [a-zA-Z0-9_]
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    '''
    Pre-Process Document Data
        - Remove All Punctuations
        - Convert to Lower Case
    '''
    def preprocess(doc_data):
        doc_data = ' '.join(tokenizer.tokenize(doc_data))
        doc_data = doc_data.lower()
        return doc_data

    '''
    Positional Index to store Data as a Dictionary of Format :
    { 
        term1 : [ (DocId1,[index1,index2,...]) , (DocId2,[index1,index2,...]) , ... ] 
        term2 : [ (DocId1,[index1,index2,...]) , (DocId2,[index1,index2,...]) , ... ] 
        .
        .
        .
    }
    '''
    positional_index = {}
    # A List to Store All File Names
    all_file_names = []

    # Obtain All Indexes of a Term in a Document
    # The position of the first word in the document by convention is taken as 1
    def term_indexes(term,doc_data):
        term_indxs_lst = []
        for i in range(len(doc_data)):
            if doc_data[i]==term:
                term_indxs_lst.append(i+1)
        return term_indxs_lst

    # Function to Create Inverted Index
    def create_positional_index(doc_data,docid):
        doc_data = doc_data.split()
        for term in doc_data:
            if term not in stopwords: # Remove this Check if you do not have a List of Stop Words
                if term not in positional_index:
                    positional_index[term] = {}
                    positional_index[term][docid] = term_indexes(term,doc_data.split())
                # Avoid Redundancy by Eliminating Indexing of Same Terms from the Same Document
                elif positional_index[term].get(docid) == docid:
                    pass
                else:
                    positional_index[term][docid] = term_indexes(term,doc_data.split())
        all_file_names.append(docid)

    '''
    Reading, Pre-Processing Document Collection and Creating Inverted Index
    It is assumed that Document Collection is in '.txt' files

    For Windows Users, Use the following line of code to open file  
        file_path = f".\{file}"
    '''
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"./{file}"
            with open(file_path, "r") as f:
                doc_data = f.read()
            doc_data = preprocess(doc_data)
            create_positional_index(doc_data,file[:-4]) # [:-4] to Remove '.txt' from FileName which will be used as DocId

    # Return the Inverted Index and List of All File Names
    return positional_index,all_file_names

