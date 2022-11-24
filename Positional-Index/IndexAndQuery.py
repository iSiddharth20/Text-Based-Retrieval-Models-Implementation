'''
Python 3.0
Retrieve Relevant Documents and Respective Indexes for a Query using 2 Phrase Query Search
'''

from PositionalIndex import Positional_IndexFn

def phrase_query(positional_index,query):
    query = query.lower().split()
    word1 = query[0]
    word2 = query[-1]
    result = {}
    if len(query)==2:
        bidirection = False
    else:
        k = int(query[1].split('/')[1])
        bidirection = True
    # Check if Both Terms are Present in the Same Document
    for docid in positional_index[word1]:
        if docid in positional_index[word2]:
            result[docid] = []
            # Check if Both Terms are Specific Distance Apart in the Same Document
            for index in positional_index[word1][docid]:
                # For 2 Phrase Query and No Provided Distance, Assume word2 is right after word1
                if bidirection==False and index+1 in positional_index[word2][docid]:
                    result[docid].append((index,index+1))
                # For 2 Phrase Query and Provided Distance
                elif bidirection == True:
                    for i in range(index-k,index+k+1):
                        if i in positional_index[word2][docid]:
                            result[docid].append((index,i))
        # Remove Null Values from Results
        if result[docid] == []:
            del result[docid]
    # If No Results are Found, Return Blank Dictionary
    if result == {}:
        return None
    return result


# Add the Relevant File/Folder Paths
stopwords_path = 'Enter The Full Path to Folder with File containing Stop Words'
stopwords_filename = 'File Name of the File with Stop Words (With Extention)'
collection_path = 'Enter The Full Path to Folder with Document Collection'

# Create Positional Index 
positional_index = Positional_IndexFn(stopwords_path,stopwords_filename,collection_path)

'''
Enter Query String as : 
    term1 /n term2
    term1 term2
Where :
    n = Max Desired Distance between term1 and term2
If NO /n is Mentioned :
    It is Assumed that for a Document to be Relevant term2 must be right after term1
Eg. :
    I student
    student /2 I
'''
query = 'Provide Query As a String Here'

# The Following Dictionary Contains All Documents Relevants and Respective Indexes to Query Retrieved through Boolean Retrieval Model
relevant_docs = phrase_query(positional_index,query)

