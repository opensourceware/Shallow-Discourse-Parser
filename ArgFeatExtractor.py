import nltk
import json
import cPickle
from conn_head_mapper import*

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

#.................................................to find root word of connective...........................................
def findHead(discourseBank):
	newdiscourseBank = discourseBank
	connectiveList=[]
	chm = ConnHeadMapper()
	for number,relation in enumerate(discourseBank):
		if relation['Type'] == 'Explicit':
			head, indices = chm.map_raw_connective(relation['Connective']['RawText'])
			discourseBank[number]['ConnectiveHead'] = head
	return discourseBank


#......................................................lca function.......................................................
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
    if b:
        lcaIndex = minLen
        return l[0][:lcaIndex]

#............................................................height function.................................................
def height(phrase):
	i = 0
	while (phrase.parent().label() != ''):
		phrase = phrase.parent()
		i+=1
	return i

#..............................................................to take path.................................................
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
#.................................................................pruning approach to get candidates..............................

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

#...................................................................... features extraction for argument classifier.....................
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


		if clause in arg2:
			label = 'Arg2'
		else:
			label = 'NULL'

		featureSet.append((featureVector, label))
	return featureSet


if __name__ == "__main__":


	predictedLabelsArg2 = []
	LabelsArg2 = []
	allFeat=[]
	temp=0

        pdtb=[]
        f = open('relations.json','r')
        for line in f:
                pdtb.append(json.loads(line))
        f.close()

        parses = json.loads(open('parses.json','r').read())

	for relation in pdtb:
		if (relation['Type'] == 'Explicit') and (relation['Arg1']['TokenList'][0][3] - relation['Arg2']['TokenList'][0][3] == -1):
			doc = relation['DocID']
			sentenceOffSet = relation['Arg2']['TokenList'][0][3]
			s = parses[doc]['sentences'][sentenceOffSet]['parsetree']
			ptree = nltk.ParentedTree.fromstring(s)
			indices = [token[4] for token in relation['Connective']['TokenList']]
			try:
				clauses = pruning(ptree, indices)
				arg2 = relation['Arg2']['RawText']
				fSet = clauseExtractFeatures(clauses, relation['ConnectiveHead'])
				allFeat=allFeat+fSet
			except IndexError as e:
				temp=temp+1
	with open('PSarg2Features.p', 'wb') as f:
		cPickle.dump(allFeat, f)
	print temp

	classifier = nltk.classify.NaiveBayesClassifier.train(fSet)
	with open('PSarg2classifier.p', 'wb') as f:
		cPickle.dump(classifier, f)
