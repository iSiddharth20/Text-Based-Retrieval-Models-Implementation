'''
Python 3.0
Pagerank Algorithm with Power Iteration (Google's Formulation)
'''

# Import Required Libraries
from collections import defaultdict

def PageRank(input_file,output_file):

    '''
    Import Page Links from Input File (input_file = FileName.txt) of Format
        NumberOfPages \n
        NumberOfLinks \n
        SourcePage[i] Destination Page[j] \n
        SourcePage[i] Destination Page[j] \n
        SourcePage[i] Destination Page[j] \n
        .
        .
        .
    '''
    with open(input_file) as f:
        filedata = f.read().split('\n')
    
    '''
    N : Number of Pages
    M : Stochastic Matrix
    R : Rank Score Vector initialized as [1/N]nxn

    links : Links between SourcePage[i] and DestinationPage[j] 
    alpha : Teleportation Number

    Formula ->
        M = alpha.M + (1-alpha).[1/N]nxn
        Iterate "R[t+1] = M.R[t]" till "R[t+1]==R[t]"
    '''
    N = int(filedata[0])
    links = filedata[2:]
    alpha = 0.15
    defval = round(float((1-alpha)/N),3)
    M = [[defval] * N] * N
    R = [float(1/N)] * N

    '''
    Map to Store Outgoing Links from Source Page to Destination Page
    '''
    link_map = defaultdict(list)
    for link in links:
        link = link.split()
        src_page = int(link[0])
        dst_page = int(link[-1])
        link_map[src_page].append(dst_page)
    
    '''
    Transform Stochastic Matrix with Teleport
    '''
    for src_page,dst_page_list in link_map.items():
        outdegree_src_page = len(dst_page_list)
        val = round(float(alpha/outdegree_src_page),3)
        for dst_page in dst_page_list:
            lst = M[dst_page].copy()
            lst[src_page] += val
            lst[src_page] = round(lst[src_page],3)
            M[dst_page] = lst
    
    '''
    Perform Iterative Multiplication "M.R" until condition "R[t+1] = R[t]" is met
    '''
    flag = True
    iterations = 0
    while(flag==True):
        Rt = []
        for i in range(N):
            lst = M[i].copy()
            vectorsum = 0
            for j in range(N):
                vectorsum += (lst[j]*R[j])
                vectorsum = round(vectorsum,3)
            Rt.append(vectorsum)
        iterations += 1
        if Rt==R:
            flag = False
        else:
            flag = True
        R = Rt

        
    '''
    Map RankVector to PageId
    Sort PageRank Scores from Highest to Lowest
    '''
    PageRanks = [[x,y] for x,y in enumerate(R)]
    PageRanks = sorted(PageRanks, key=lambda x: x[1], reverse=True)

    '''
    Save the Final Page Ranks to Output File (output_file = FileName.txt) in the Format
        Rank : 1 , PageId : -- , PageRank Score : --
        Rank : 2 , PageId : -- , PageRank Score : --
        Rank : 3 , PageId : -- , PageRank Score : --
        .
        .
        .
    '''
    FinalRank = 1
    with open(output_file, 'w') as f:
        for PageId, Rank in PageRanks:
            OutputString = 'Rank : ' + str(FinalRank).zfill(2) + ' , PageId : ' + str(PageId) + ' , PageRank Score : ' + str(Rank) + '\n'
            f.write(OutputString)
            FinalRank += 1


input_file = 'Enter The Full Path and FileName.txt'
output_file = 'Enter The Full Path and FileName.txt'
PageRank(input_file,output_file)

