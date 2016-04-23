import nltk
from nltk.corpus import stopwords
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


def getproductionRules(ptree):
	childLabel=[]
	for child in ptree:
		if type(child) == unicode:
			return
		getproductionRules(child)
		childLabel.append(child.label())
	feature = (ptree.label(), tuple(childLabel))
	if feature in productionRules:
		productionRules[feature] += 1
	else:
		productionRules[feature] = 1
	return
	

def getdependencyRules(dependencies):
	for rule in dependencies:
        if (rule[1].split('-')[0] in stopSet) or (rule[2].split('-')[0] in stopSet):
            continue
		dRule = rule[0]
		if rule[1][-1] < rule[2][-1]:
			orientation = 'right'
		else:
			orientation = 'left'
		feature = (dRule, orientation)
		if feature not in dependencyRules.keys():
			dependencyRules[feature] = 1
		else:
			dependencyRules[feature] += 1


if __name__ == '__main__':
	#features=[]
    stopSet = stopwords.words("english")
	pdtb = cPickle.load(open('pdtb.p','r'))
	#subjectivity = json.loads(open('mpqa_subj_05.json').read())
	dependencyRules={}
	productionRules={}
	parses = json.loads(open('pdtb-parses.json').read())
	for doc in parses:
	#	featureList={}
	#	getsubjectivityFeatures()
		for sentence in parses[doc]['sentences']:
			ptree = sentence['parsetree']
			ptree = nltk.ParentedTree.fromstring(ptree)
			dependencies = sentence['dependencies']
			getdependencyRules(dependencies)
			getproductionRules(ptree)
	#	featureList.append
    dependencyRules2 = dependencyRules
    productionRules2 = productionRules
    for item in dependencyRules:
        if (dependencyRules[item] <= 10):
            dependencyRules2.pop(item)
    for item in productionRules:
        if (productionRules[item] <= 10) or (productionRules[item] >= 70):
            productionRules2.pop(item)
	cPickle.dump(dependencyRules2, open('dependencyRules.p','wb'))
	cPickle.dump(productionRules2, open('productionRules.p','wb'))
