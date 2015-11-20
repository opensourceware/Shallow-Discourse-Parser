# -*- coding: utf-8 -*-
"""
Created on Oct 18 2015

@author: manpreet
"""

import json
import connExtractFeat
import conn_head_mapper as ConnectiveHeadMapper
import nltk
import cPickle
import connMatching

def findHead(discourseBank):
	newdiscourseBank = discourseBank
	connectiveList=[]
	chm = ConnectiveHeadMapper()
	for relation,number in enumerate(discourseBank):
		if relation['Type'] == 'Explicit':
			head, indices = chm.map_raw_connective(relation['Connective']['RawText'])
			discourseBank[number]['ConnectiveHead'] = head


def extractFeatures(pdtb, parses):
	relationId = 0
	featureSet=[]
	for doc in parses:
		for sentence in parses[doc]['sentences']:
			indices = []
			for num, word in enumerate(sentence['words']):
				if num in indices:
					continue
				for link in word[1]['Linkers']:
					if 'conn' in link:
						if relationId == link[5:]:
							break
						else:
							relationId = link[5:]
							for relation in pdtb:
								if str(relation['ID']) == relationId:
									indices = [conn[4] for conn in relation['Connective']['TokenList']]
									rawtext = relation['Connective']['RawText']
									#connHead = relation['ConnectiveHead']
									ptree = sentence['parsetree']
									ptree = nltk.ParentedTree.fromstring(ptree)
									if ptree.leaves() == []:
										break
									else:
										featureSet.append((connExtractFeat.getfeatures(ptree, indices),'Y'))
									break
							break
				if len(word[1]['Linkers']) != 0:
					if link == word[1]['Linkers'][-1] and ('conn' not in word[1]['Linkers'][-1]):
						if ((len(word[1]['Linkers']) == 1) and ('conn' not in word[1]['Linkers'][0])) or ((len(word[1]['Linkers']) > 1)):
							ptree = sentence['parsetree']
							ptree = nltk.ParentedTree.fromstring(ptree)
							rawtext, connHead = connMatching.matchConnective(ptree, word[0], num)
							leaves = ptree.leaves()
							if rawtext != '':
								rawwords = rawtext.split()
								try:
									indices = [leaves.index(rawword) for rawword in rawwords]
								except ValueError:
									if len(rawwords) == 1:
										indices = [num]
									else:
										indices.append(leaves.index(rawword.capitalize()))
										for rawword in rawwords[1:]:
											indices.append(leaves.index(rawword))
									featureSet.append((connExtractFeat.getfeatures(ptree, indices),'N'))


if __name__ == '__main__':

	global featureSet
	featureSet = []
	pdtb = cPickle.load(open('pdtb.p', 'rb'))
	parses = json.loads(open('pdtb-parses.json').read())
	#pdtb = cPickle.load(open('dev.p', 'rb'))
	#parses = json.loads(open('dev-parses.json').read())

	extractFeatures(pdtb, parses)

	cPickle.dump(featureSet, open('connFeatures.p','wb'))

	#classifier = nltk.classify.NaiveBayesClassifier.train(trainSet)
	#print nltk.classify.accuracy(classifier, testSet)


