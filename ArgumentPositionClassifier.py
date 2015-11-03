
import argPositionFeat
import nltk
import json
import cPickle
import conn_head_mapper

def constructFeatures(discourseBank,treeBank):
    featureSet=[]
    for relation in discourseBank:
        if relation['Type']=='Explicit':
            arg1Set=set()
            arg2Set=set()
            arg1Tokens=[]
            arg2Tokens=[]
            for i in relation['Arg1']['TokenList']:
                arg1Set.add(i[3])
                #arg1Tokens.append(i[4])
            for i in relation['Arg2']['TokenList']:
                arg2Set.add(i[3])
                #arg2Tokens.append(i[4])
            
            arg1=list(arg1Set)
            arg2=list(arg2Set)
            arg1.sort()
            arg2.sort()
            #print arg1Set, arg2Set
            if arg1[-1] < arg2[0]:
                label='PS'
            
            if (len(arg1Set)==1 and len(arg2Set)==1):
                if (arg1Set.pop()==arg2Set.pop()):
                    label='SS'
            
            connective=relation['Connective']['TokenList']
            connectiveRawText = relation['Connective']['RawText']
            #print relation
            #chm= conn_head_mapper.ConnHeadMapper()
            #head,connectiveTokens = chm.map_raw_connective(relation['Connective']['RawText'])
                    
            #connectiveStartValue=relation['Connective']['TokenList'][0][4]
            #connectiveTokens=[i+connectiveStartValue for i in connectiveTokens]            
            
            sentenceOffset=connective[0][3]
            connectiveTokens=[token[4] for token in connective]            
            doc=relation['DocID']
            ptree=treeBank[doc]['sentences'][sentenceOffset]['parsetree']
            ptree = nltk.ParentedTree.fromstring(ptree)
            if ptree.leaves() != []:
                featureSet.append((argPositionFeat.getFeatures(ptree, connectiveRawText, connectiveTokens), label))
                #print featureSet
    return featureSet



if __name__=="__main__":
    pdtb = cPickle.load(open('pdtb.p','r'))
    parses = json.loads(open('pdtb-parses.json').read())
    devpdtb = cPickle.load(open('dev.p', 'r'))
    devparses = json.loads(open('dev-parses.json').read())
    featureSets = constructFeatures(pdtb, parses)
    cPickle.dump(featureSets, open('argPosFeatures2.p','wb'))
    devfeatureSets = constructFeatures(devpdtb, devparses)
    cPickle.dump(devfeatureSets, open('devargPosFeatures2.p','wb'))

    classifier = nltk.classify.NaiveBayesClassifier.train(featureSets)

    #classifier.prob_classify_many()
    print nltk.classify.accuracy(classifier, devfeatureSets)
