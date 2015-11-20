# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 2015

@author: shubham
"""

import nltk

def root2leaf(ptree,location,i,flist):
        
    h = location.__len__()
    if i == h :
        return flist 
    else:
        flist.append(ptree[location[i]].label())
        ptree = ptree[location[i]]
        i+=1
        return root2leaf(ptree,location,i,flist)
    
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
                

def checkVP(ptree):
    c=False
    #print ptree.label()
    if ptree.label() == 'VP':
        return True
    #nltk.ParentedTree.
    if ptree.height() == 2:   #child nodes
        #print ptree.parent()
        return False
    for child in ptree:
        c= c or checkVP(child)
    return c

def checkTR(ptree):
    c=False
    #print ptree.treeposition()
    if ptree.label() == 'T':
        return True
    if ptree.height() == 2:   #child nodes
        #print ptree.parent()
        return False
    for child in ptree:
        c= c or checkTR(child)
    return c


def getfeatures(ptree, leaf_index):

    leave_list = ptree.leaves()
    #print leaf_index, len(leave_list)     
    if len(leaf_index) > 1:
        lca_loc = lca(ptree,leaf_index)
    else:
        lca_loc = ptree.leaf_treeposition(leaf_index[0])[:-1]
    
    selfcategory = ptree[lca_loc].label()
    parentcategory = ptree[lca_loc].parent().label()
    
    
    
    #location = ptree.leaf_treeposition(leaf_index)
    flist = []
    r2l = root2leaf(ptree,lca_loc,0,flist)
       
    #location = location[:-1]

    leftSibling = ptree[lca_loc].left_sibling()
    if leftSibling != None:
	leftSibling = leftSibling.label()

    rightSibling = ptree[lca_loc].right_sibling()
    rightVP = False
    rightTR = False
    if rightSibling != None:
        rightVP = checkVP(rightSibling)
        rightTR = checkTR(rightSibling)
	rightSibling = rightSibling.label()
    
    #print r2l, lsibling, rsibling, selfcategory, parentcategory, rightVP, rightTR
    
    prev = leaf_index[0] - 1
    next = leaf_index[len(leaf_index)-1] + 1

    pl = ptree.pos()
    cPOS = selfcategory
    c = ' '.join(leave_list[leaf_index[0]:leaf_index[-1]+1])
    c = c.lower()

    if prev >= 0:
        prevC = [pl[prev][0], c ]
        prevC=','.join(prevC)
        prevPOS = pl[prev][1] 
        prevPOScPOS = [pl[prev][1],cPOS]
        prevPOScPOS=','.join(prevPOScPOS)
    else:
        prevC = ['NONE',c]
        prevC=','.join(prevC)
        prevPOS = 'NONE'
        prevPOScPOS = ['NONE',cPOS]
        prevPOScPOS=','.join(prevPOScPOS)
        
    sentenceLength = len(leave_list)
    if next < sentenceLength:
        nextC = [pl[next][0], c]
        nextC=','.join(nextC) 
        nextPOS = pl[next][1]  
        nextPOScPOS = [pl[next][1], cPOS]
        nextPOScPOS=','.join(nextPOScPOS)
    else:
        nextC = ['NONE',c]
        nextC=','.join(nextC)
        nextPOS = 'NONE'
        nextPOScPOS = ['NONE',cPOS]
        nextPOScPOS=','.join(nextPOScPOS)
    
    # root2leaf compressed
    r2lcomp = r2l    
    x=0
    while x < len(r2lcomp)-1 :
        if r2lcomp[x] == r2lcomp[x+1]:
            del r2lcomp[x+1]
        else:
            x += 1

    feat = {'connective':c, 'connectivePOS':cPOS, 'prevWord':prevC, 'prevPOSTag':prevPOS, 'prevPOS+cPOS':prevPOScPOS,'nextWord':nextC,'nextPOSTag':nextPOS,'cPOS+nextPOS':nextPOScPOS,'root2LeafCompressed':','.join(r2lcomp),'root2Leaf':','.join(r2l),'leftSibling':leftSibling,'rightSibling':rightSibling,'parentCategory':parentcategory,'boolVP':rightVP,'boolTrace':rightTR}  

    return feat



if __name__=="__main__":
    s = "(S (PP (IN For) (NP (DT the) (NN moment))) (PRN (, ,) (ADVP (IN at) (JJS least)) (, ,)) (NP (NN euphoria)) (VP (VBZ has) (VP (VBN replaced) (NP (NP (NN anxiety)) (PP (IN on) (NP (NNP Wall) (NNP Street)))))) (. .))"
    tree = nltk.ParentedTree.fromstring(s)
    getfeatures(tree,[3])


