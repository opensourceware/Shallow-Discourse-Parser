import nltk
import conn_head_mapper
import json
import cPickle
import codecs

def lca(ptree,tokens):
    n = len(tokens)
    
    l=[ptree.leaf_treeposition(i) for i in tokens]
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

def featureRelation(discourseBank,treeBank):
    featureLabelList = ['Temporal.Asynchronous.Precedence',
		'Temporal.Asynchronous.Succession', 
		'Temporal.Synchrony', 
		'Contingency.Cause.Reason',
		'Contingency.Cause.Result',
		'Contingency.Condition', 
		'Comparison.Contrast',
		'Comparison.Concession',
		'Expansion.Conjunction',
		'Expansion.Instantiation',
		'Expansion.Restatement',
		'Expansion.Alternative',
		'Expansion.Alternative.Chosen alternative',
		'Expansion.Exception',
		'EntRel',
		]
    chm=conn_head_mapper.ConnHeadMapper()
    countSS = 0

    for relation in discourseBank:
        #print relation['DocID']
        if relation['Type']=='Explicit':
            arg1Cluster = []
            arg2Cluster = []
	    arg1 = relation['Arg1']['RawText'].split()
	    arg2 = relation['Arg1']['RawText'].split()
	    for word in arg1:
		    if word in brownClusters:
			arg1Cluster.append(word)
	    for word in arg2:
		    if word in brownClusters:
			arg2Cluster.append(word)
            cartesianProduct = [(a,b) for a in arg1Cluster for b in arg2Cluster]

	    featureLabel = relation['Sense'][0]
            if featureLabel in featureLabelList:
                connective=relation['Connective']['TokenList']
                connectiveRaw=relation['Connective']['RawText']
                connectiveWord,connectiveTokens=chm.map_raw_connective(connectiveRaw)  
                
                connectiveStartValue=connective[0][4]
                sentenceOffset=connective[0][3]
                leaf_index=[i+connectiveStartValue for i in connectiveTokens]
                
                doc=relation['DocID']
                tree=parses[doc]['sentences'][sentenceOffset]['parsetree']
                ptree = nltk.ParentedTree.fromstring(tree)
                if ptree.leaves() != []:
                    if len(leaf_index) > 1:
                        lca_loc = lca(ptree,leaf_index)
                    else:
                        lca_loc = ptree.leaf_treeposition(leaf_index[0])[:-1]
                
                    connectivePOS=ptree[lca_loc].label()
                    if leaf_index[0]==0:
                        connectivePrev=None
                    else:
                        connectivePrev=parses[doc]['sentences'][sentenceOffset]['words'][leaf_index[0]-1][0]
                   
                    featureVector={'Connective':connectiveWord,'ConnectivePOS':connectivePOS,'ConnectivePrev':connectivePrev,'WordPairFeatures':cartesianProduct}
		    featureLabel = relation['Sense']
		    featureSet.append((featureVector, featureLabel))
                    
   
    return featureSet
    
    
    
if __name__=="__main__":
    #pdtbdev=[json.loads(x) for x in open('/home/shubham/shallow-discourse-parsing/conll15-st-dev-2015-03-04/pdtb-data.json')]
    pdtb = cPickle.load(open('pdtb.p','r'))    
    #parsesdev=json.loads(open('/home/shubham/shallow-discourse-parsing/conll15-st-dev-2015-03-04/pdtb-parses.json').read())    
    parses =json.loads(open('pdtb-parses.json').read())    
    
    fset=featureRelation(pdtb,parses)
    cPickle.dump(fset,open('senseFeatures.p','wb'))
    #fset = cPickle.load(open('senseFeatures.p','r'))


    trainSet,testSet=fset[100:],fset[:100]   

    labels=[]
    test=[] 
    for features in testSet:
        test.append(features[0])
        labels.append(features[1])
        
    #print labels 
    
    #print classifier.classify_many(test)    
    
    classifier = nltk.classify.NaiveBayesClassifier.train(trainSet)
    print nltk.classify.accuracy(classifier, testSet)
