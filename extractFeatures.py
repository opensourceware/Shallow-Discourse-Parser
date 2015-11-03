# -*- coding: utf-8 -*-
"""
Created on Sunday 11 Oct 2015

@author: manpreet
"""
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



def getsubjectivityFeatures(relation):
	subjectivityStrengthArg1 = 0
	subjectivityStrengthArg2 = 0
	arg1 = relation['Arg1']['RawText'].upper().split()
	arg2 = relation['Arg2']['RawText'].upper().split()
	for word in arg1:
		if word in subjectivity.keys():
			if subjectivity[word] == [u'negative', u'strongsubj']:
				subjectivityStrengthArg1 += -2
			if subjectivity[word] == [u'negative', u'weaksubj']:
				subjectivityStrengthArg1 += -1
			if subjectivity[word] == [u'positive', u'weaksubj']:
				subjectivityStrengthArg1 += 1
			if subjectivity[word] == [u'negative', u'weaksubj']:
				subjectivityStrengthArg1 += 2
	for word in arg2:
		if word in subjectivity.keys():
			if subjectivity[word] == [u'negative', u'strongsubj']:
				subjectivityStrengthArg2 += -2
			if subjectivity[word] == [u'negative', u'weaksubj']:
				subjectivityStrengthArg2 += -1
			if subjectivity[word] == [u'positive', u'weaksubj']:
				subjectivityStrengthArg2 += 1
			if subjectivity[word] == [u'negative', u'weaksubj']:
				subjectivityStrengthArg2 += 2
	featureSet[-1]['subjectivityStrengthArg1'] = subjectivityStrengthArg1
	featureSet[-1]['subjectivityStrengthArg2'] = subjectivityStrengthArg2


def parseFeatures(relation):
	global productionRules
	global dependencyRules
	doc = relation['DocID']
	arg1sentenceOffSet=[]
	arg1sentenceOffSet.append(relation['Arg1']['TokenList'][0][3])
	for token in relation['Arg1']['TokenList']:
		if arg1sentenceOffSet[-1]!=token[3]:
			arg1sentenceOffSet.append(token[3])
	for sentenceOffSet in arg1sentenceOffSet:
		arg1ptree = parses[doc]['sentences'][sentenceOffSet]['parsetree']
		dependencies = parses[doc]['sentences'][sentenceOffSet]['dependencies']
		ptree = nltk.ParentedTree.fromstring(arg1ptree)
		leaf_index=[]
		for token in relation['Arg1']['TokenList']:
			if sentenceOffSet == token[3]:
				leaf_index.append(token[4])
		prevelem = leaf_index[0]-1
		index = 0
		for elem in leaf_index:
			if (prevelem+1) != elem:
				index=leaf_index.index(elem)
				break
			else:
				prevelem=elem
		if index==0:
			try:
				lca_loc2 = lca(ptree, leaf_index)
				ptree2 = ptree[lca_loc2]
				getproductionRules(ptree2)
			except IndexError as e:
				print e.message
		else:
			try:
				lca_loc1 = lca(ptree, leaf_index)
				ptree1 = ptree[lca_loc1]
				getproductionRules(ptree1)
			except IndexError as e:
				print e.message
			try:
				lca_loc2 = lca(ptree, leaf_index)
				ptree2 = ptree[lca_loc2]
				getproductionRules(ptree2)
			except IndexError as e:
				print e.message
		dependencyRule=[]
		leaves = ptree.leaves()
		if index!=0:
			leaves = leaves[leaf_index[0]:leaf_index[index-1]+1] + leaves[leaf_index[index]:leaf_index[-1]]
		for dependency in dependencies:
			if (dependency[1][:-2] in leaves) and (dependency[2][:-2] in leaves):
				dependencyRule.append(dependency)
		dependencies = dependencyRule
		getdependencyRules(dependencies)
	arg1productionRules=productionRules
	arg1dependencyRules=dependencyRules
	arg2sentenceOffSet=[]
	arg2sentenceOffSet.append(relation['Arg2']['TokenList'][0][3])
	for token in relation['Arg2']['TokenList']:
		if arg2sentenceOffSet[-1]!=token[3]:
			arg2sentenceOffSet.append(token[3])
	productionRules=[]
	dependencyRules=[]
	for sentenceOffSet in arg2sentenceOffSet:
		arg2ptree = parses[doc]['sentences'][sentenceOffSet]['parsetree']
		ptree = nltk.ParentedTree.fromstring(arg2ptree)
		dependencies = parses[doc]['sentences'][sentenceOffSet]['dependencies']
		leaf_index=[]
		for token in relation['Arg2']['TokenList']:
			if sentenceOffSet == token[3]:
				leaf_index.append(token[4])
		prevelem = leaf_index[0]-1
		index = 0
		for elem in leaf_index:
			if (prevelem+1) != elem:
				index=leaf_index.index(elem)
				break
			else:
				prevelem=elem
		if index==0:
			try:
				lca_loc2 = lca(ptree, leaf_index)
				ptree2 = ptree[lca_loc2]
				getproductionRules(ptree2)
			except IndexError as e:
				print e.message
		else:
			try:
				lca_loc1 = lca(ptree, leaf_index)
				ptree1 = ptree[lca_loc1]
				getproductionRules(ptree1)
			except IndexError as e:
				print e.message
			try:
				lca_loc2 = lca(ptree, leaf_index)
				ptree2 = ptree[lca_loc2]
				getproductionRules(ptree2)
			except IndexError as e:
				print e.message
		dependencyRule=[]
		leaves = ptree.leaves()
		leaves = leaves[leaf_index[0]:leaf_index[index-1]+1] + leaves[leaf_index[index]:leaf_index[-1]]
		for dependency in dependencies:
			if (dependency[1][:-2] in leaves) and (dependency[2][:-2] in leaves):
				dependencyRule.append(dependency)
		dependencies = dependencyRule
		getdependencyRules(dependencies)
	arg2productionRules=productionRules
	arg2dependencyRules=dependencyRules
	featureVector={}
	for feature in featureList:
		featureVector[feature]=None
	for feature in arg1productionRules:
		if feature in arg2productionRules:
			featureVector[feature]='both'
		else:
			featureVector[feature]='arg1'
	for feature in arg2productionRules:
		if feature not in arg1productionRules:
			featureVector[feature]='arg2'
	for feature in arg1dependencyRules:
		if feature in arg2dependencyRules:
			featureVector[feature]='both'
		else:
			featureVector[feature]='arg1'
	for feature in arg2dependencyRules:
		if feature not in arg1dependencyRules:
			featureVector[feature]='arg2'
	labelSet.append(relation['Sense'])
	featureSet.append(featureVector)



def getproductionRules(ptree):
	childLabel=[]
	for child in ptree:
		if type(child) == unicode:
			return
		getproductionRules(child)
		childLabel.append(child.label())
	feature = (ptree.label(), tuple(childLabel))
	if feature not in productionRules:
		productionRules.append(feature)
	return


def getdependencyRules(dependencies):
	for rule in dependencies:
		dRule = rule[0]
		if rule[1][-1] < rule[2][-1]:
			orientation = 'right'
		else:
			orientation = 'left'
		feature = (dRule, orientation)
		if feature not in dependencyRules:
			dependencyRules.append(feature)



if __name__ == '__main__':
	#features=[]
	pdtb = cPickle.load(open('dev.p','r'))
	parses = json.loads(open('dev-parses.json').read())
	subjectivity = json.loads(open('mpqa_subj_05.json').read())
	featureSet=[]
	labelSet=[]
	dependencyRules=[]
	productionRules=[]
	#for doc in parses:
	#	featureList={}
	#	getsubjectivityFeatures()
	featureList = cPickle.load(open('featureList.p', 'rb'))
	for relation in pdtb:
		productionRules=[]
		dependencyRules=[]
		if (relation['Type'] == 'Explicit') or (relation['Type'] == 'Implicit'):
			parseFeatures(relation)
			getsubjectivityFeatures(relation)
	f = open('devImplicitFeatures.p','wb')
	cPickle.dump(featureSet, f)
	f.close()
	f = open('devLabelSet.p','wb')
	cPickle.dump(labelSet, f)
	f.close()


