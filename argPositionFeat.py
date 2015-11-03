import nltk
import conn_head_mapper

def lca(ptree,leaf_index):
    n = len(leaf_index)
    
    l=[ptree.leaf_treeposition(i) for i in leaf_index]
    minLen=min(map(len,l))
    b = True
    for i in range(minLen):
        for j in range(n-1):
            if l[j][i] !=l[j+1][i]:
                b = False                
                lcaIndex=i-1
                return l[j][:i]
                #return lcaIndex
                
    if b:
        lcaIndex = minLen
        return l[0][:lcaIndex]
        #return lcaIndex

def getFeatures(ptree, c, leaf_index):
        
    leaves = ptree.leaves()
    chm = conn_head_mapper.ConnHeadMapper()
    head, connectiveHead_index = chm.map_raw_connective(c)
    connectiveHead_index = [leaf_index[i] for i in connectiveHead_index]

    if len(connectiveHead_index) > 1:
        lca_loc = lca(ptree, connectiveHead_index)
    else:
        lca_loc = ptree.leaf_treeposition(connectiveHead_index[0])[:-1]
    
    cPOS = ptree[lca_loc].label()
    #parentcategory = ptree[lca_loc].parent().label()
        
    #location = location[:-1]
    sentenceLen = len(leaves)
    m1 = sentenceLen*(1/3)
    m2 = sentenceLen*(2/3)

    if connectiveHead_index[len(connectiveHead_index)/2] < m1:
        cPosition = 'START'
    elif connectiveHead_index[len(connectiveHead_index)/2] >= m1 and connectiveHead_index[len(connectiveHead_index)/2] < m2:
        cPosition = 'MIDDLE'
    else:
        cPosition = 'END'

    prev = leaf_index[0] - 1
    prev2 = prev - 1
    #nextt = leaf_index[len(leaf_index)-1] + 1

    pl = ptree.pos()

    #f1 = cPOS    
    if prev >= 0:
        prevC = [pl[prev][0], head]
        prevC=', '.join(prevC)
        prevPOS = pl[prev][1] 
        prevPOScPOS = [pl[prev][1],cPOS]
        prevPOScPOS=', '.join(prevPOScPOS)
        prev = pl[prev][0]
    else:
        prevC = ['NONE', head]
        prevC=', '.join(prevC)
        prevPOS = 'NONE'
        prevPOScPOS = ['NONE',cPOS]
        prevPOScPOS=', '.join(prevPOScPOS)
        prev = 'NONE'
        
    if prev2 >= 0:
        prev2C = [pl[prev2][0],head]
        prev2C=', '.join(prev2C)
        prev2POS = pl[prev2][1] 
        prev2POScPOS = [pl[prev2][1],cPOS]
        prev2POScPOS=', '.join(prev2POScPOS)
        prev2 = pl[prev2][0]
        
    else:
        prev2C = ['NONE', head]
        prev2C=', '.join(prev2C)
        prev2POS = 'NONE'
        prev2POScPOS = ['NONE',cPOS]
        prev2POScPOS=', '.join(prev2POScPOS)
        prev2 = 'NONE'
      
    feat = {'connective':head, 'connectivePOS':cPOS,'cPosition':cPosition, 'prevWord+c':prevC, 'prevPOSTag':prevPOS, 'prevPOS+cPOS':prevPOScPOS,'prevWord':prev,'prev2Word+c':prev2C, 'prev2POSTag':prev2POS, 'prev2POS+cPOS':prev2POScPOS,'prevWord':prev2}
    
    return feat
          
     

if __name__=="__main__":
    s = "(S (PP (IN For) (NP (DT the) (NN moment))) (PRN (, ,) (ADVP (IN at) (JJS least)) (, ,)) (NP (NN euphoria)) (VP (VBZ has) (VP (VBN replaced) (NP (NP (NN anxiety)) (PP (IN on) (NP (NNP Wall) (NNP Street)))))) (. .))"
    #s = parsesdev['wsj_2276']['sentences'][1]['parsetree'] 
    #s=s[2:-3]
#    s = "(ROOT (S (NP (JJ Congressional) \
#    (NNS representatives)) (VP (VBP are) (VP (VBN motivated) \
#    (PP (IN by) (NP (NP (ADJ shiny) (NNS money))))))) (. .))"
    #s=u"( (S (NP (NP (DT The) (NN group) (POS 's)) (NN resilience)) (VP (VBZ gets) (NP (PRP$ its) (JJ first) (NN test)) (NP (NN today)) (SBAR (WHADVP (WRB when)) (S (NP (CD 30) (JJ top) (NN pilot) (NN union) (NNS leaders)) (VP (VB convene) (PP (IN outside) (NP (NNP Chicago))) (PP (IN in) (NP (DT a) (ADJP (RB previously) (VBN scheduled)) (NN meeting))))))) (. .)) )\n"
    tree = nltk.ParentedTree.fromstring(s)
    getFeatures(tree,[4])
