
import argPositionFeat
import nltk
import json
import cPickle
import conn_head_mapper
from confusion_matrix import*

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



def fscore_conf(classifier,testSet):
	conf_obj=ConfusionMatrix()
        true_label=[]
        predicted_label=[]
        for i in testSet:
        	true_label.append(i[1])
		predicted_label.append(classifier.classify(i[0]))
	conf_obj.add_list(predicted_label,true_label)
	conf_obj.print_matrix()
	f1_score=conf_obj.compute_average_f1()
	print 'F1 score = ',f1_score,'\n'	








if __name__=="__main__":
        trainpdtb = cPickle.load(open('/home/f2012687/temp_SDP_master_codes/pdtb.p','r'))
        trainparses = json.loads(open('/home/f2012687/temp_SDP_master_codes/pdtb-parses.json').read())
        devpdtb = cPickle.load(open('/home/f2012687/temp_SDP_master_codes/dev.p', 'r'))
        devparses = json.loads(open('/home/f2012687/temp_SDP_master_codes/dev-parses.json').read())

        trainfeatureSet = constructFeatures(trainpdtb, trainparses)
        cPickle.dump(trainfeatureSet, open('argPosFeatures.p','wb'))
        devfeatureSet = constructFeatures(devpdtb, devparses)
        #cPickle.dump(devfeatureSet, open('devargPosFeatures2.p','wb'))
	#classifier = nltk.classify.NaiveBayesClassifier.train(trainfeatureSet)
	classifier=nltk.MaxentClassifier.train(trainfeatureSet)
	print '......................................ON TRAINING DATA..................','\n'
	fscore_conf(classifier,trainfeatureSet)
	print 'Accuracy = ',nltk.classify.accuracy(classifier, trainfeatureSet),'\n'

	print '......................................ON DEVELOPMENT DATA..................','\n'
	fscore_conf(classifier,devfeatureSet)
	print 'Accuracy = ',nltk.classify.accuracy(classifier, devfeatureSet),'\n'


    #classifier.prob_classify_many()
