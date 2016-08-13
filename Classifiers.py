
import nltk
import connExtractFeat
import argPositionFeat
import finalArgsExtractor
import explicitSenseFeat
#import semantic

def matchConnectiveList(wordList,wordNum):
    wordStructure=wordList[wordNum]
    
    word=wordStructure[0]
    word=word.lower()
    singleConnectiveWordList=['accordingly','additionally','after','afterward','also','alternatively', 'although', 'and','because','besides', 'but','consequently','conversely','earlier','else','except','finally','further','furthermore','hence','however','indeed','instead','later','lest','likewise','meantime','meanwhile','moreover','nevertheless','next','nonetheless','nor','once','or','otherwise','overall','plus','previously','rather','regardless','separately','similarly','simultaneously','since','specifically','still','then','thereafter', 'thereby', 'therefore', 'though', 'thus', 'till', 'ultimately', 'unless', 'until','whereas', 'while', 'yet']
    multipleConnectiveWordList=['as','before','by','for','either','if','in','insofar','much','neither','now','on','so','when']
    wordListLength=len(wordList)    
    if word in singleConnectiveWordList:
        return word,0
    elif word in multipleConnectiveWordList:
        if wordNum==wordListLength-1:
            if word in ['as','before','for','if','so']:
                return word,0
            else:
                return 'False',0
        wordNextStructure=wordList[wordNum+1]
        wordNext=wordNextStructure[0]
        wordNext.lower()
        
        
        if word=='as':
            if wordNext=='a':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='result':
                    return 'as a result',2
                else:
                    return 'False',0
            elif wordNext=='an':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='alternative':
                    return 'as an alternative',2
                else:
                    return 'False',0
            elif wordNext=='if':
                return 'as if',1
            elif wordNext=='long':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='as':
                    return 'as long as',2
                else:
                    return 'False',0
            elif wordNext=='soon':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='as':
                    return 'as soon as',2
                else:
                    return 'False',0 
            elif wordNext=='though':
                return 'as though',1 
            elif wordNext=='well':
                return 'as well',1
            else:
                return 'as',0
        elif word=='before':
            if wordNext=='and':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='after':
                    return 'before and after',2
                else:
                    return 'False',0
            else:
                return 'before',0
        elif word=='by':
            if wordNext=='comparison':
                return 'by comparison',1
            elif wordNext=='contrast':
                return 'by contrast',1 
            else:
                return 'by',0
        elif word=='for':
            if wordNext=='example':
                return 'for example',1
            elif wordNext=='instance':
                return 'for instance',1
            else:
                return 'for',0
        elif word=='if':
            for i in range(wordNum,wordListLength):
                if(wordList[i][0].lower()=='then'):
                    print "ho rha hai"
                    skip=i-wordNum
                    return 'if then',skip
            if wordNext=='and':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='when':
                    return 'if and when',2 
                else:
                    return 'False',0
            else:
                return 'if',0
        elif word == 'in':
            if wordNext=='addition':
                return 'in addition',1
            elif wordNext=='contrast':
                return 'in contrast',1
            elif wordNext=='fact':
                return 'in fact',1
            elif wordNext=='other':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='words':
                    return 'in other words',2
                else:
                    return 'False',0
            elif wordNext=='particular':
                return 'in particular',1
            elif wordNext=='short':
                return 'in short',1
            elif wordNext=='sum':
                return 'in sum',1
            elif wordNext=='the':
                if (wordNum+1)!=(wordListLength-1):
                    wordNextNextStructure=wordList[wordNum+2]
                    wordNextNext=wordNextNextStructure[0]
                    wordNextNext.lower()
                    if wordNextNext=='end':
                        return 'in the end',2
                    else:
                        return 'False',0
                else:
                    return 'False',0
            elif wordNext=='turn':
                return 'in turn',1
            else:
                return 'False',0
        elif word=='insofar':
            if wordNext=='as':
                return 'insofar as',1
            else:
                return 'False',0
        elif word=='much':
            if wordNext == 'as':
                return 'much as',1
            else:
                return 'False',0
        elif word=='now':
            if wordNext=='that':
                return 'now that',1
            else:
                return 'False',0
        elif word=='on':
            if wordNext=='the':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='contrary':
                    return 'on the contrary',2
                elif wordNextNext=='other':
                    return 'on the other hand',3
                else:
                    return 'False',0
            else:
                return 'False',0
            
        elif word=='so':
            if wordNext=='that':
                return 'so that',1
            else:
                return 'so',0
        elif word=='when':
            if wordNext =='and':
                wordNextNextStructure=wordList[wordNum+2]
                wordNextNext=wordNextNextStructure[0]
                wordNextNext.lower()
                if wordNextNext=='if':
                    return 'when and if',2
                else:
                    return 'False',0
            else:
                return 'when',0
        elif word=='neither':
            for i in range(wordNum,wordListLength):
                if(wordList[i][0].lower()=='nor'):
                    skip=i-wordNum
                    return 'neither nor',skip
            return 'False',0
                
        elif word=='either':
            for i in range(wordNum,wordListLength):
                if(wordList[i][0].lower()=='or'):
                    skip=i-wordNum
                    return 'either or',skip
            return 'False',0
                

    else:
        return 'False',0


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
        
def classifyConnective(sentence,wordNum,connClassifier):

    parsetree = nltk.ParentedTree.fromstring(sentence['parsetree'])
    """
    wordList=parsetree.leaves()
    word=wordList[wordNum]
    wordString,connHead=connMatching.matchConnective(parsetree,word,wordNum)
    indices=[]
    for word in wordString:
        if word in wordList:
            indices.append(wordList.index(word))
    #print 'conn ',wordString
    """
    wordList=sentence['words']
    wordString,skip=matchConnectiveList(wordList,wordNum)

    if wordString=='False':
        return 'False','N',0
    else:
         
         if parsetree.leaves()!=[]:                        
             connLabel=connClassifier.classify(connExtractFeat.getfeatures(parsetree,range(wordNum,wordNum+skip+1)))
             #connLabel=connClassifier.classify(connExtractFeat.getfeatures(parsetree,indices))
             return wordString,connLabel,skip
         else:
             return 'False','N',0

        
def classifyOther(sentence,wordString,wordNum,skip,argPosClassifier,senseClassifier,argClassifier):
    wordList=sentence['words']
    parsetree = nltk.ParentedTree.fromstring(sentence['parsetree'])

    if parsetree.leaves()!=[]:                        
       	leaf_index=range(wordNum,wordNum+skip+1)
	c=wordString.strip()

	"""
	c = ""
	for i in (leaf_index):
	        if i == 0:
	        	c = c + parsetree[parsetree.leaf_treeposition(i)]
        	else:
			c = c + " " + parsetree[parsetree.leaf_treeposition(i)]  
	c=c.strip()
	leave_list = parsetree.leaves() 
        s=''
        for i in leave_list:
            if i in [',','.','!','?','%','(',')','$','#','@','*','^'] or i[0] in ["'",'"','`']:
                s=s+i
            else:
                s=s+' '+i
            
        s = s.encode('utf-8')
        semantic_feat = semantic.semantic_features(s)
	"""

	fv1 = argPositionFeat.getFeatures(parsetree,c,leaf_index)
        argPosLabel=argPosClassifier.classify(fv1)
	
        argDict=finalArgsExtractor.argsExtract(argClassifier,parsetree,leaf_index)

        arg1string=argDict['arg1']
        arg2string=argDict['arg2']
	arg1string=arg1string.replace(' ,',',')
	arg2string=arg2string.replace(' ,',',')
	arg1string=arg1string.replace('`` ' , '"')
	arg2string=arg2string.replace('`` ' , '"')
	while u" n't" in arg1string:
		arg1string = arg1string.replace(" n't", "n't")

	while u" n't" in arg2string:
                arg2string = arg2string.replace(" n't", "n't")

	while u" 's" in arg1string:
                arg1string = arg1string.replace(" 's", "'s")

	while u" 's" in arg2string:
                arg2string = arg2string.replace(" 's", "'s")

	arg1=[]
	arg2=[]
	leaves=parsetree.leaves()
	arg1words=argDict['arg1'].split()
	arg2words=argDict['arg2'].split()
	ind = -1

	string = ' '.join(leaves)
	if ' '.join(arg1words[:2]) in string:
		ind = string.index(' '.join(arg1words[:2]))
		ind = len(string[:ind].split())-1
		if ind == 0:
			ind = -1

	for word in arg1words:
		ind += leaves[ind+1:].index(word)+1
		arg1.append(ind)

	ind = -1
	if ' '.join(arg2words[:2]) in string:
		ind = string.index(' '.join(arg2words[:2]))
		ind = len(string[:ind].split())-1
		if ind == 0:
			ind = -1

	arg2words=argDict['arg2'].split()
	for word in arg2words:
		ind += leaves[ind+1:].index(word)+1
		arg2.append(ind)


#	leaves=parsetree.leaves()
#	arg1words=argDict['arg1'].split()
#	for word in arg1words:
#		arg1.append(leaves.index(word))		
#	
#	arg2words=argDict['arg2'].split()
#	for word in arg2words:
#		arg2.append(leaves.index(word))

	fv2=explicitSenseFeat.featureExtraction(parsetree,leaf_index,sentence,argDict,c)
        #senseFeatureVector.update(semantic_feat)
        senseLabel=senseClassifier.classify(fv2)
    return argPosLabel,senseLabel,arg1,arg2


