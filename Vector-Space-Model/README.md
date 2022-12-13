# Vector Space Model
***

+ Python 3.0
+ Required Dependencies : nltk (Only for RegexpTokenizer)
+ Can add Custom Stop Words List
+ CreateIndex.py : 
    - Creates Required Index
    - Creates Champion List
    - Creates Cluster Pruning Index
+ TopK.py : 
    - Retrieves Exact Top K Documents through Cosine Similarity Score
    - Retrieves In-Exact Top K Documents through Cosine Similarity Score and Champions List
    - Retrieves In-Exact Top K Documents through Cosine Similarity Score and Cluster Pruning Index

***

### Vector Space Model with Exact Top-K Retrieval using Cosine Similarity
+ TopK.py : 
    - Creates Index through CreateIndex.py 
    - Retreieves a List of K Relevant Documents for a String Query using Cosine Similarity over the Original Corpus and Index

***

### Vector Space Model with In-Exact Top-K Retrieval using Champions List
+ TopK.py : 
    - Creates Champion List through CreateIndex.py 
    - Retreieves a List of K Relevant Documents for a String Query using Cosine Similarity over Original Corpus and Champion List

***

### Vector Space Model with In-Exact Top-K Retrieval using Cluster Pruning Index
+ TopK.py : 
    - Creates Cluster Pruning Index through CreateIndex.py 
    - Retreieves a List of K Relevant Documents for a String Query using Cosine Similarity over Modified Corpus and Cluster Pruning Index

***

### Comments Added for Better Understanding