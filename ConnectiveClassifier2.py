import json
import connExtractFeat
import conn_head_mapper as ConnectiveHeadMapper
import nltk

def findHead(discourseBank):
	newdiscourseBank = discourseBank
	connectiveList=[]
	chm = ConnectiveHeadMapper()
	for relation,number in enumerate(discourseBank):
		if relation['Type'] == 'Explicit':
			head, indices = chm.map_raw_connective(relation['Connective']['RawText']
			connectiveList.append(head)
			newdiscourseBank[number]['ConnectiveHead'] = head
	return connectiveList, newdiscourseBank



def extractFeatures(newdiscourseBank, parses, connectiveList):
	featureList = {}
	featureSet = []
	docList = parses.keys()
	docList.sort()
	
	relationId = 0
	for doc in docList:
		for sentence in parses[doc]['sentences']:
			for word in sentence['words']:
				for link in word[1]['Linkers']:
					if 'conn' in link:
						if relationId == link[5:]
							break
						else:
							relationId = link[5:]
							break
							for relation in pdtb:
								if relation['ID'] == relationId:
									indices = [conn[4] for conn in relation['Connective']['TokenList']]
									rawtext = relation['Connective']['RawText']
									break
							ptree = sentence['parsetree']
							featureSet.append((connExtractFeat.getfeatures(ptree, indices),'Y')
					else:
						leaves = sentence['parsetree'].leaves()
						connective, incides = matchConnective(leaves, word)



def matchConnective(ptree, word):
	singleConnectiveWordList=['accordingly','additionally','after','afterward','also','alternatively', 'although', 'and','because','besides', 'but','consequently','conversely','earlier','else','except','finally','further','furthermore','hence','however','indeed','instead','later','lest','likewise','meantime','meanwhile','moreover','nevertheless','next','nonetheless','nor','once','or','otherwise','overall','plus','previously','rather','regardless','separately','similarly','simultaneously','since','specifically','still','then','thereafter', 'thereby', 'therefore', 'though', 'thus', 'till', 'ultimately', 'unless', 'until','whereas', 'while', 'yet']
	multipleWordConnectiveList = ['as','before','by','for','either','if','in','insofar','later','much','neither','now','on','so','when']

	if word in singleWordConnectiveList:
		return word, [0]
	elif word in multipleWordConnectiveList:
		leaves = ptree.leaves()
		index = leaves.index(word)
		lca_loc = ptree.leaf_treeposition(index)
		leftSibling = ptree[lca_loc].left_sibling()
		rightSibling = ptree[lca_loc].right_sibling()
		leftWord = leaves[index-1]
		rightWord = leaves[index+1]
		cPrev = leftWord + ' ' + word
		for connective in connectiveList:
			while(cPrev in connective):
				leftWord = leaves.index(leftWord)-1
				cPrev = leftWord + ' ' + cPrev
			indexleftWord = leaves.index(leftWord)
			lca_loc_leftWord = ptree.leaf_treeposition(index)
			leftWordPOS = ptree[lca_loc_leftWord].label()
			if leftWordPOS 



			#wordList = [word[0] for word in sentence['words']]
			#connectiveWord, indices = matchConnectiveList(wordList, len(wordList))

			

			#if result == None:
			#	featureList, featureLabel = None, 'N'
			#else:
			#	ptree = sentence['parsetree']
			#	featureList = connExtractFeat.getFeatures(ptree, indices)

			
			#linker = sentence['words'][indices[0]][1]['Linkers']
			#for link in linker:
			#	if 'conn' in link:
			#		relationId = link[5:]
			#for relation in pdtb:
			#	if relation['ID'] == relationId && relation['Type'] == 'Explicit':
			#		featureLabel = 'Y'
			#	else:
			#		featureLabel = 'N'

			#featureSet.append((featureList, featureLabel))

parses=json.loads(open('pdtb-parses.json').read())
pdtb=cPickle.load(open('pdtb.p','rb'))
























