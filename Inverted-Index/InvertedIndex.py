'''
Python 3.0
Build Inverted Index

stopwords_path = 'Enter The Full Path to Folder with File containing Stop Words'
stopwords_filename = 'File Name of the File with Stop Words (With Extention)'
collection_path = 'Enter The Full Path to Folder with Document Collection'

'''
# Importing Necessary Libraries
import os
import nltk

# Tokenizer to keep only Alpha-Numeric Words  [a-zA-Z0-9_]
tokenizer = nltk.RegexpTokenizer(r"\w+")

def PreProcess(doc_data):
    doc_data = ' '.join(tokenizer.tokenize(doc_data))
    doc_data = doc_data.lower()
    return doc_data

def Inverted_Index_Fn(stopwords_path,stopwords_filename,collection_path):
    '''
    Inverted Index to store Data as a Dictionary of Format :
    { 
        term1 : [ DocId1 , DocId2 , ... ] 
        term2 : [ DocId1 , DocId2 , ... ] 
        .
        .
        .
    }
    '''
    inverted_index = {}
    
    # Getting StopWords from a File (Optional)
    '''
    For Windows Users, Use the following line of code to open file  
        with open(path+'\'+filename) as f:
    '''
    with open(stopwords_path+'/'+stopwords_filename) as f:
        stopwords = f.read().split('\n')
        
    #Changing Working Directory to the Folder that contains Document Collection 
    os.chdir(collection_path)

    '''
    Pre-Process Document Data
        - Remove All Punctuations
        - Convert to Lower Case
    '''

    # Function to Create Inverted Index
    def create_inverted_index(doc_data,docid):
        doc_data = doc_data.split()
        for term in doc_data:
            if term not in stopwords: # Remove this Check if you do not have a List of Stop Words 
                if term not in inverted_index:
                    inverted_index[term] = []
                    inverted_index[term].append(docid)
                # Avoid Redundancy by Eliminating Indexing of Same Terms from the Same Document
                elif docid in inverted_index[term]:
                    pass
                else:
                    inverted_index[term].append(docid)

    '''
    Reading, Pre-Processing Document Collection and Creating Inverted Index
    It is assumed that Document Collection is in '.txt' files
    '''
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"./{file}"
            with open(file_path, "r") as f:
                doc_data = f.read()
            doc_data = PreProcess(doc_data)
            create_inverted_index(doc_data,file[:-4]) # [:-4] to Remove '.txt' from FileName which will be used as DocId

    # Return the Inverted Index
    return inverted_index
