'''
Python 3.0
PyLucene 8.11.0
Create Required PyLucene Index
Retrieve Top-K Relevant Document for String Query
'''

# Importing Necessary Libraries
import os
import nltk
import math
from collections import defaultdict
import lucene
from java.io import File
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader, Term
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.util import BytesRefIterator

# Add the Relevant File/Folder Paths
stopwords_path = 'Enter The Full Path to Folder with File containing Stop Words'
stopwords_filename = 'File Name of the File with Stop Words (With Extention)'
collection_path = 'Enter The Full Path to Folder with Document Collection'
index_path = 'Enter The Full Path to Folder where PyLucene Index will be Stored'

# Tokenizer to keep only Alpha-Numeric Terms  [a-zA-Z0-9_]
tokenizer = nltk.RegexpTokenizer(r"\w+")

# Initializa JVM
lucene.initVM()

'''
Pre-Process Document Data, Query String
     - Remove All Punctuations
     - Remove Stopwords (Optional)
     - Convert to Lower Case
'''
def PreProcess(data):
    data = tokenizer.tokenize(data)
    data = [token for token in data if token not in stopwords] # Skip this Line if No Stopwords Are Imported
    data = ' '.join(data)
    data = data.lower()
    return data

# Transform Query to Vector
def QueryVectorGenerator(query):
        query = PreProcess(query)
        queryTerms = query.split()
        queryVector = defaultdict(lambda: 0)
        for term in queryTerms:
            queryVector[term] += 1
        return queryVector

# Transform Document to Vector in order of Query Vector and Terms
def DocumentVectorGenerator(docId, queryVector):
        documentVector = {}
        for term in queryVector.keys():
            documentVector[term] = TermFreequencyInDoc(term, docId)
        return documentVector

# Return a List of All Documents that contain the Term
def DocsWithTerm(term):
    termQuery = TermQuery(Term('DocData', term))
    hits = searcher.search(termQuery, lnCorpus).scoreDocs
    docIds = []
    i = 0
    while i < len(hits):
        docIds.append(hits[i].doc)
        i = i + 1
    return docIds

# Calculate TF Value
def TermFreequencyInDoc(termText, docId):
    termsList = indexReader.getTermVector(int(docId), 'DocData')
    terms = termsList.iterator()
    for term in BytesRefIterator.cast_(terms):
        dpEnum = terms.postings(None)
        dpEnum.nextDoc()
        tf = dpEnum.freq()
        if tf!=0:
            return tf
    return 0

# Calculate IDF Value
def idf(term):
    tf = indexReader.docFreq(Term('DocData', PreProcess(term)))
    return math.log((lnCorpus + 1) /(tf + 1), 10)

# Calculate TF-IDF Value
def tfidf(idf, wtd):
    return idf * wtd

# Transform Vector to TF-IDF for a given Document
def VectorToTFIDF(vector, docId):
    for term in vector.keys():
        # Calculate Term Weight
        tf = TermFreequencyInDoc(term, docId)
        if tf == 0:
            wt = 0
        else:
            wt = 1 + math.log(float(tf), 10)
        vector[term] = tfidf(idf(term), wt)
    return vector

# Transform Query Vector to TF-IDF
def QueryVectorToTFIDF(queryVector):
    for term, tf in queryVector.items():
        queryVector[term] = tfidf(idf(term), 1 + math.log(tf, 10))
    return queryVector

# Compute Cosine Similarity Score with L2 Normalization
def computeCosine(vector1, vector2):
    len_v1 = len(vector1)
    len_v2 = len(vector2)
    # Make Both Vectors of Same Length
    if len_v1 != len_v2:
        if len_v1 > len_v2:
            for i in range(len_v1 - len_v2):
                vector2.append(0)
        else:
            for i in range(len_v2 - len_v1):
                vector1.append(0)
    # Calculate Cross Product
    sq_v1 = 0
    sq_v2 = 0
    crossProduct = 0
    for i in range(len(vector1)):
        crossProduct = crossProduct + vector1[i] * vector2[i]
        sq_v1 += math.pow(vector1[i], 2)
        sq_v2 += math.pow(vector2[i], 2)
    # Calculate Cosine Similarity Score
    cs = crossProduct / ((math.sqrt(sq_v1) * math.sqrt(sq_v2)))
    return cs

# Create PyLucene Index
def Create_IndexFn(indexpath,collectionpath,stopwords_path,stopwords_filename):

    # Getting StopWords from a File (Optional)
    global stopwords
    '''
    For Windows Users, Use the following line of code to open file  
        with open(path+'\'+filename) as f:
    '''
    with open(stopwords_path+stopwords_filename) as f:
        stopwords = f.read().split('\n')

    # Specify the Path where Index will be Stored
    global indexPath
    indexPath = File(indexpath).toPath()
    global indexDir
    indexDir = FSDirectory.open(indexPath)

    # Specify Analyser and Index Writer Configuration
    global writerConfig
    writerConfig = IndexWriterConfig(StandardAnalyzer())
    global writer
    writer = IndexWriter(indexDir, writerConfig)
    
    # Set Field Parameter for DocumentName,DocumentId
    field_filename = FieldType()
    field_filename.setStored(True)
    field_filename.setTokenized(False)
    field_filename.setIndexOptions(IndexOptions.DOCS)
    
    # Set Field Parameter for DocumentData   
    field_filedata = FieldType()
    field_filedata.setStored(True)
    field_filedata.setTokenized(True)
    field_filedata.setStoreTermVectors(True)
    field_filedata.setStoreTermVectorPositions(True)
    field_filedata.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)

    # Change Working Directory to Collection Path
    os.chdir(collectionpath)
    
    # Import and Pre-Process the Document Collection
    for file in os.listdir():
        docId = 0
        if file.endswith(".txt"):
            file_path = f"./{file}"
            with open(file_path, "r") as f:
                doc_data = f.read()
            # Add DocumentId and Pre-Processed Document Data to PyLucene Index
            if len(doc_data)>0:
                doc_data = PreProcess(doc_data)
                doc = Document()
                doc.add(Field('DocName', str(file[:-4]), field_filename))
                doc.add(Field('DocId', docId, field_filename))
                doc.add(Field('DocData', doc_data, field_filedata))
                writer.addDocument(doc)
                docId += 1
    
    # Initialize Index Reader and Searcher
    global indexReader
    global searcher
    global lnCorpus
    indexReader = DirectoryReader.open(writer)
    searcher = IndexSearcher(indexReader)
    lnCorpus = indexReader.numDocs()

# Retrieve Top-K Relevant Documents for Specified Query
def TopKRetrieval(query, k):
    queryVector = QueryVectorGenerator(query)
    docIds = []
    docVectors = {}
    computedSimilarity = []
    topKDocInformation = {}
    
    # Get Documents with the Term
    for term in queryVector.keys():
        docIds += DocsWithTerm(term)

    # Create Vector for Documents
    for docId in docIds:
        docVectors[docId] = DocumentVectorGenerator(docId, queryVector)

    # Transform Document Vectors to TF-IDF Values
    for docId, vector in docVectors.items():
        docVectors[docId] = VectorToTFIDF(vector, docId)

    # Transform Query Vector to TF-IDF Values
    queryVector = QueryVectorToTFIDF(queryVector)

    # Compute Cosine Similarity Scores
    for docId, vector in docVectors.items():
        computedSimilarity.append({"DocId": docId, "CosineSimilarityScore": computeCosine(list(queryVector.values()), list(vector.values()))})
    computedSimilarity = sorted(computedSimilarity, key=lambda docIndex: docIndex["CosineSimilarityScore"],reverse=True)

    # Print Top-K RetrievedDocuments
    i = 0
    while i < k and k < len(computedSimilarity):
        DocName = searcher.doc(computedSimilarity[i]['DocId']).get('DocName')
        print(DocName, str(computedSimilarity[i]['DocId']))
        topKDocInformation[computedSimilarity[i]['DocId']] = docVectors[computedSimilarity[i]['DocId']]
        i += 1
    return topKDocInformation


Create_IndexFn(index_path,collection_path,stopwords_path,stopwords_filename)
query = 'Provide Query As a String Here'
k = 10 # Change this to Required Integer Value
Results = TopKRetrieval(query, k)

