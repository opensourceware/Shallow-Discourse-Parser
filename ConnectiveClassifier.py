# -*- coding: utf-8 -*-
"""
Created on Oct 18 2015

@author: manpreet
"""


import json
from conn_head_mapper import ConnHeadMapper
import connExtractFeat
import nltk
import cPickle as pickle 
from fscore import*

#def getFeatureVector()

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
        
            
            
    
    
    
def findHead(discourseBank):
    discourseBankNew=discourseBank
    connectiveList=set()
    chm= ConnHeadMapper()
    for num,relations in enumerate(discourseBank):
        if relations['Type']=='Explicit':
            head,_=chm.map_raw_connective(relations['Connective']['RawText'])
            connectiveList.add(head)
            discourseBankNew[num]['ConnectiveHead']=head
    return discourseBankNew,connectiveList

def dataProcess(discourseBank,treeBank,connectiveList):
    featureSets=[]
    docList=treeBank.keys()
    docList.sort()
    totalDiscourses=len(discourseBank)
    lastDiscourse=totalDiscourses-1
    #print totalDiscourses
    dBIterator=0
    oldExplicitIterator=dBIterator
    explicit=0
    oldexplicit=explicit
    i=0;j=0;k=0
    for doc in docList:
        
        sentenceList=treeBank[doc]['sentences']
        for sentenceOffset,sentence in enumerate(sentenceList):
            
            wordList=sentence['words']
            #print wordList
            lengthWordList=len(wordList)
            wordNum=0
            while(wordNum<lengthWordList):
                wordStructure=wordList[wordNum]
                word=wordStructure[0]
                word=word.lower()
                #print word
                wordDictionary=wordStructure[1]
                #print wordDictionary     
                #if not matchConnectiveList(connectiveList,word):
                #    continue
                relation=discourseBank[dBIterator]
                #print relation['Type']
                
                while(1): 
                    #print 'Consecutive:%d'%dBIterator 
                    if(relation['Type']=='Explicit' or dBIterator==lastDiscourse):
                        break
                    
                    dBIterator+=1
                    relation=discourseBank[dBIterator]
                    if (relation['Type']=='Explicit'):
                        connective=relation['ConnectiveHead']
                        #print 1,explicit,connective
                        explicit+=1
                    #print relation['Type']
                    
                
                docWord=int(doc[4:]);docConnective=int(relation['DocID'][4:])
                cOBWord=wordDictionary['CharacterOffsetBegin']
                cOEWord=wordDictionary['CharacterOffsetEnd']
                
                if relation['Type']=='Explicit':
                    connective=relation['ConnectiveHead']
                    connectiveLength=len(relation['Connective']['CharacterSpanList'])
                    cOBConnective=relation['Connective']['CharacterSpanList'][0][0]
                    cOEConnective=relation['Connective']['CharacterSpanList'][connectiveLength-1][1]
                
                if ((docConnective > docWord) or (docWord==docConnective and cOEWord<cOBConnective)):
                    
#                    if word=='in':
#                        print doc,sentenceOffset
#                        print sentence
#                        print relation
                    result,skip=matchConnectiveList(wordList,wordNum)
                    
                    #if relation['Type']=='Explicit' and explicit==40:
                    #    print 1,explicit,word,connective
                    if result!='False':
                        #print 3,word,result,connective
                        label='N'
                        tokenNo=range(wordNum,wordNum+skip+1)
                        #tokenNo=[words[4] for words in tokenNumberLists]
                        tokens=[token[0] for token in wordList]
                        #if word=='either':
                            #print sentenceList[sentenceOffset-1]
                            #print word,wordNum
                            #print tokens
                        #print relation
                        parsetree = nltk.ParentedTree.fromstring(sentence['parsetree'])
                        if parsetree.leaves()!=[]:                        
                            featureSets.append((connExtractFeat.getfeatures(parsetree,tokenNo),label))
                    wordNum+=skip
                    
                elif((docWord==docConnective) and ( cOBConnective <= cOBWord and cOEWord <= cOEConnective)):
                    #Important match the potential connectives to connective head and not connectives' raw text                    
                    l=connective.split()
                    l=[string.lower() for string in l]
                    if(word in l):
                        #better thing would have been to just match the character offset beginning and end of connective
                        result,skip=matchConnectiveList(wordList,wordNum)
                        
                        
                        if result=='if then':
                            print 1,word,l,result,connective
                        if result!='False':
                            label='Y'
                            tokenNumberLists=relation['Connective']['TokenList']
                            tokenNo = range(wordNum, wordNum+skip+1)
                            #tokenNo=[words[4] for words in tokenNumberLists]
                            ##tokens=[token[0] for token in wordList]
                            #print tokens,tokenNo,word
                            #print relation
                            parsetree = nltk.ParentedTree.fromstring(sentence['parsetree'])
                            if parsetree.leaves()!=[]:
#                                print sentence['parsetree']                                
#                                print doc,word,sentenceOffset
#                                print tokens
#                                print relation
                                featureSets.append((connExtractFeat.getfeatures(parsetree,tokenNo),label))
                            
                            
                            if (explicit-oldexplicit>1):
#                                print explicit
#                                print doc,word,connective
#                                
#                                print discourseBank[oldExplicitIterator]
#                                print relation
                                
                                k+=1
                            oldexplicit=explicit
                            oldExplicitIterator=dBIterator
                        
                            
                            #if relation['Type']=='Explicit' and explicit==40:
                            #    print 2,explicit,word,connective
                            #print explicit,word,connective
                            i+=1
                        wordNum+=skip
                            
                    else:
                        #these lines are not required. they are the cases in which a word appears before the connective head
                        result,skip=matchConnectiveList(wordList,wordNum)
                        #print 2,word,l,result,connective
                        wordNum+=skip
                        if result!='False':
                            label='N'
                        
                    j+=1
                    
                    
                            #getFeatureVector()
                elif((docConnective < docWord) or (docConnective==docWord and cOEConnective<cOBWord)):
                    #if relation['Type']=='Explicit' and explicit==40:                    
                    #    print 3,explicit,word,connective,sentenceOffset                 
                    if (dBIterator > totalDiscourses):
                        print 'kuch galat hai'  
                    if dBIterator!=lastDiscourse:
                        dBIterator+=1
                        relation=discourseBank[dBIterator]
                        if (relation['Type']=='Explicit'):
                            #print 2,explicit,connective
                            explicit+=1
                        wordNum-=1
                #print doc,sentenceOffset,wordNum,cOBWord,word
                wordNum+=1         
                    #print i,dBIterator
                  
    print i,j,k
    return featureSets
   
                
            
    
if __name__=="__main__":
    #pdtb=[json.loads(x) for x in open('/home/shubham/shallow-discourse-parsing/conll15-st-train-2015-03-04/pdtb-data.json')]
    #pdtbdev=[json.loads(x) for x in open('/home/abhishek/Desktop/coNLL/shallow-discourse-parsing/conll15-st-dev-2015-03-04/pdtb-data.json')]
    #parsesdev=json.loads(open('/home/abhishek/Desktop/coNLL/shallow-discourse-parsing/conll15-st-dev-2015-03-04/pdtb-parses.json').read())
    #pdtbdevNew,_=findHead(pdtb)
    
        trainpdtb = pickle.load(open('/home/f2012687/temp_SDP_master_codes/pdtb.p','r'))
        trainparses=json.loads(open('/home/f2012687/temp_SDP_master_codes/pdtb-parses.json').read())    
        trainpdtbNew,connectiveList=findHead(trainpdtb)
        connectiveList=list(connectiveList)
        featureSets=dataProcess(trainpdtbNew,trainparses,connectiveList)
        pickle.dump(featureSets, open('connFeatures.p','wb'))

   
        devpdtb = pickle.load(open('/home/f2012687/temp_SDP_master_codes/dev.p', 'rb'))
        devparses = json.loads(open('/home/f2012687/temp_SDP_master_codes/dev-parses.json').read())

        print '....................................................................TRAINING..................', 
        #classifier = nltk.classify.NaiveBayesClassifier.train(featureSets)
        classifier=nltk.MaxentClassifier.train(featureSets)
        print '....................................................................ON TRAINING DATA..................',
        testSet=featureSets
        fscore(classifier,testSet)
        print 'ACCURACY= ',nltk.classify.accuracy(classifier, testSet),'\n',

        print '....................................................................ON DEVELOPMENT DATA..................',
        devpdtbNew,connectiveList=findHead(devpdtb)
        connectiveList=list(connectiveList)
        testSet=dataProcess(devpdtbNew,devparses,connectiveList)
        fscore(classifier,testSet)
        print 'ACCURACY= ',nltk.classify.accuracy(classifier, testSet),'\n',
