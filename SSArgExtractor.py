import nltk
import json
import cPickle

discourseAdverbial = ['accordingly', 'additionally', 'afterwards', 'also', 'alternatively', 'as a result',
'as an alternative', 'as well', 'besides', 'by comparison', 'by contrast',
'by then', 'consequently', 'conversely', 'earlier', 'either..or', 'except', 'finally',
'for example', 'for instance', 'further', 'furthermore', 'hence', 'in addition',
'in contrast', 'in fact', 'in other words', 'in particular', 'in short', 'in sum',
'in the end', 'in turn', 'indeed', 'instead', 'later', 'likewise', 'meantime',
'meanwhile', 'moreover', 'nevertheless', 'next', 'nonetheless',
'on the contrary', 'on the other hand', 'otherwise', 'overall', 'previously',
'rather', 'regardless', 'separately', 'similarly', 'simultaneously', 'specifically',
'still', 'thereafter', 'thereby', 'therefore', 'thus', 'ultimately', 'whereas'
]


coordinatingConnective = ['and', 'but', 'else', 'if then', 'neither nor', 'nor',
'on the one hand on the other hand', 'or', 'plus', 'then', 'yet']


subordinatingConnective = ['after', 'although', 'as', 'as if', 'as long as', 'as soon as', 'as though', 'because',
'before', 'before and after', 'for', 'however', 'if', 'if and when', 'insofar as',
'lest', 'much as', 'now that', 'once', 'since', 'so', 'so that', 'though', 'till', 'unless',
'until', 'when', 'when and if', 'while']


def clauseProcessing(string):
	string = string.strip()

	punct = [' ...', ' ,', ' :', ' ;', ' ?', ' !', ' -', ' ~', ' .']
	for item in punct:
		while item in string:
			string = string.replace(item, item.strip())

	symbols = ['$ ', '# ', ' %']
	for item in symbols:
		while item in string:
			string = string.replace(item, item.strip())

	appos = [" 's", " n't", " 're"]
	for item in appos:
		while item in string:
			string = string.replace(item, item.strip())

brackets = ['-LRB- ', '-LCB- ', '-RRB-', '-RCB-']
	for item in brackets:
		while item in string:
			if item == '-LRB- ':
				string = string.replace(item, ' (')
			if item == '-RRB-':
				string = string.replace(item, ')')
			if item == '-LCB- ':
				string = string.replace(item, ' {')
			if item == '-RCB-':
				string = string.replace(item, '}')

	return string


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

def height(phrase):
	i = 0
	while (phrase.parent().label() != ''):
		phrase = phrase.parent()
		i+=1
	return i


def path(conn, clause):
	if height(conn) == height(clause):
		return conn.label()+'U'+conn.parent().label()+'D'+clause.label()
	elif height(conn) > height(clause):
		distance = height(conn)-height(clause)+1
		p = conn.label()
		parent = conn
		while (distance != 0):
			parent = parent.parent()
			p += 'U'+parent.label()
			distance -= 1
		distance = height(clause) - height(parent)
		parent = clause
		down = []
		while (distance != 0):
			parent = parent.parent()
			down.append(parent.label())
			distance -= 1
		down = down.reverse()
		if down == []:
			for item in down:
				d = 'D'+item
		d = 'D'+clause.label()
		p += d
		return p


def pruning(ptree, indices):
	clauses = []
	leaves = ptree.leaves()
	if len(indices) == 1:
		lca_loc = ptree.leaf_treeposition(indices[0])[:-1]
	else:
		lca_loc = lca(ptree, indices)
		connLastWord = ptree.leaf_treeposition(indices[-1])[:-1]
		connFirstWord = ptree.leaf_treeposition(indices[0])[:-1]
		clause = ptree[connFirstWord]
		while (clause.left_sibling() != None):
			clause = clause.left_sibling()
			clauses.insert(0, ((clause, 'left')))
		clause = ptree[connLastWord]
		while (clause.right_sibling() != None):
			clause = clause.right_sibling()
			clauses.append((clause, 'right'))
	clause = ptree[lca_loc]

	while (clause.parent().label() != ''):
		currclause = clause
		while (clause.left_sibling() != None):
			clause = clause.left_sibling()
			clauses.insert(0, ((clause, 'left')))
		clause = currclause
		while (clause.right_sibling() != None):
			clause = clause.right_sibling()
			clauses.append((clause, 'right'))
		clause = clause.parent()
	return clauses


def clauseExtractFeatures(clauses, connHead):

	featureSet = []
	if len(indices) == 1:
		lca_loc = ptree.leaf_treeposition(indices[0])[:-1]
		c = ptree[lca_loc]
		leftSibNo = 0
		while (c.left_sibling() != None):
			c = c.left_sibling()
			leftSibNo += 1
		c = ptree[lca_loc]
		rightSibNo = 0
		while (c.right_sibling() != None):
			c = c.right_sibling()
			rightSibNo += 1
		connective = ptree[lca_loc]
	else:
		lca_loc = lca(ptree, indices)
		connLastWord = ptree.leaf_treeposition(indices[-1])[:-1]
		connFirstWord = ptree.leaf_treeposition(indices[0])[:-1]
		c = ptree[connFirstWord]
		leftSibNo = 0
		while (c.left_sibling() != None):
			c = c.left_sibling()
			leftSibNo += 1
		c = ptree[connLastWord]
		rightSibNo = 0
		while (c.right_sibling() != None):
			c = c.right_sibling()
			rightSibNo += 1
#		leaves = ptree.leaves()
#		head = [leaves.index(item) for item in connHead.split(' ')]
#		lca_loc = lca(ptree, head)
		connective = ptree[lca_loc]


	if connHead in discourseAdverbial:
		connCat = 'Discourse Adverbial'
	elif connHead in coordinatingConnective:
		connCat = 'Coordinating'
	elif connHead in subordinatingConnective:
		connCat = 'Subordinating'
	else:
		connCat = None

	for item in clauses:
		clauseRelPosition = item[1]

		clause = item[0]
		clausePOS = clause.label()
		clauseParentPOS = clause.parent().label()
		if clause.left_sibling() != None:
			clauseLSPOS = clause.left_sibling().label()
		else:
			clauseLSPOS = 'NULL'
		if clause.right_sibling() != None:
			clauseRSPOS = clause.right_sibling().label()
		else:
			clauseRSPOS = 'NULL'
		clauseContext = clausePOS+'-'+clauseParentPOS+'-'+clauseLSPOS+'-'+clauseRSPOS

		conn2clausePath = path(connective, clause)

		featureVector = {'connectiveString':connHead, 'connectivePOS':connective.label(), 'leftSibNo':leftSibNo, 'rightSibNo':rightSibNo, 'connCategory':connCat, 'clauseRelPosition':clauseRelPosition, 'clausePOS':clausePOS, 'clauseContext':clauseContext, 'conn2clausePath':conn2clausePath}

		leaves = clause.leaves()
		clause = ' '.join(leaves)
		punctuation = ['...', ',', ':', ';', '?', '!', '-', '~', '.']
		for p in punctuation:
			if p in clause:
				index = clause.index(p)
				if clause[index-1] == ' ':
					clause = clause[:index-1]+clause[index:]
		appos = ["'s", "n't"]
		for item in appos:
			if item in clause:
				index = clause.index(item)
				if clause[index-1] == ' ':
					clause = clause[:index-1]+clause[index:]

		if clause in arg1:
			label = 'Arg1'
		elif clause in arg2:
			label = 'Arg2'
		else:
			label = 'NULL'

		featureSet.append((featureVector, clause))
	return featureSet

#global featureSet
#featureSet = []

if __name__ == "__main__":

	predictedLabelsArg1 = []
	LabelsArg1 = []
	predictedLabelsArg2 = []
	LabelsArg2 = []
	trainSet = cPickle.load(open('SSFeatures.p','r'))
	classifier = nltk.classify.NaiveBayesClassifier(trainSet)
	pdtb = cPickle.load(open('dev.p', 'r'))
	parses = json.loads(open('dev-parses.json').read())
	for relation in pdtb:
		if (relation['Type'] == 'Explicit') and (relation['Arg1']['TokenList'][0][3] == relation['Arg2']['TokenList'][0][3]):
			doc = relation['DocID']
			sentenceOffSet = relation['Arg1']['TokenList'][0][3]
			s = parses[doc]['sentences'][sentenceOffSet]['parsetree']
			ptree = nltk.ParentedTree.fromstring(s)
			indices = [token[4] for token in relation['Connective']['TokenList']]
			try:
				clauses = pruning(ptree, indices)
				arg1 = relation['Arg1']['RawText']
				arg2 = relation['Arg2']['RawText']
				fSet = clauseExtractFeatures(clauses, relation['ConnectiveHead'])
				devFeatures = []
				clauses = []
				for item in fSet:
					devFeatures.append(item[0])
					clauses.append(item[1])
				l = classifier.classify_many(devFeatures)
				Arg1 = ''
				Arg2 = ''
				for num, label in enumerate(l):
					if label=='Arg1':
						Arg1 += clauses[num]+' '
					elif label=='Arg2':
						Arg2 += clauses[num]+' '
				Arg1 = clauseProcessing(Arg1)
				Arg2 = clauseProcessing(Arg2)
				predictedLabelsArg1.append(Arg1)
				LabelsArg1.append(arg1)
				predictedLabelsArg2.append(Arg2)
				LabelsArg2.append(arg2)
			except IndexError as e:
				print relation
				print ptree
				print indices

	#print sklearn.metrics.f1_score(predictedLabelsArg1, LabelsArg1, average='weighted')
	#print sklearn.metrics.f1_score(predictedLabelsArg2, LabelsArg2, average='weighted')
	cPickle.dump(predictedLabelsArg1, open('predictedLabelsArg1.p','wb'))
	cPickle.dump(LabelsArg1, open('LabelsArg1.p','wb'))
	cPickle.dump(predictedLabelsArg2, open('predictedLabelsArg2.p','wb'))
	cPickle.dump(LabelsArg2, open('LabelsArg2.p','wb'))

#LabelsArg2=cPickle.load(open('LabelsArg2.p','r'))
#predictedLabelsArg2=cPickle.load(open('predictedLabelsArg2.p','r'))
#LabelsArg1=cPickle.load(open('LabelsArg1.p','r'))
#predictedLabelsArg1=cPickle.load(open('predictedLabelsArg1.p','r'))

#for num, item in enumerate(LabelsArg2):
#     if item != predictedLabelsArg2[num]:
#             print str(num)+'\t'+item+'\t'+predictedLabelsArg2[num]

#for num, item in enumerate(LabelsArg1):
#     if item != predictedLabelsArg1[num]:
#             print str(num)+'\t'+item+'\t'+predictedLabelsArg1[num]

