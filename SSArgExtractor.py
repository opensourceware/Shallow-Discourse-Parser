import nltk
import josn
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
	if len(indices) == 1:
		lca_loc = ptree.leaf_treeposition(indices[0])[:-1]
	else:
		lca_loc = lca(ptree, indices)
	clause = ptree[lca_loc]
	clauses.append(clause)
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


def clauseExtractFeatures(clauses, connHead, ptree, agr1, arg2):

	for clause in clauses:
		if (len(clause) == 1):
			connective = clauses.pop(clauses.index(clause))
			break
	c = connective
	i = 0
	while (c.left_sibling() != None):
		c = c.left_sibling()
		leftSibNo += 1
	i = 0
	c = connective
	while (c.right_sibling() != None):
		c = c.right_sibling()
		rightSibNo += 1

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

		conn2clausePath = path(conn, clause)

		featureVector = {'connectiveString':conn, 'leftSibNo':leftSibNo, 'rightSibNo':rightSibNo, 'connCategory':connCat, 'clauseRelPosition':clauseRelPosition, 'clauseContext':clauseContext, 'conn2clausePath':conn2clausePath}

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

		featureSet.append((featureVector, label))


if __name__ == "__main__":
	pdtb = 
	parses = 
	global featureSet
	featureSet = []

	for relation in pdtb:
		if relation['Type'] == 'Explicit':
			if (relation['Arg1']['TokenList'][0][3] == relation['Arg2']['TokenList'][0][3]):
				doc = relation['DocID']
				sentenceOffSet = relation['Arg1']['TokenList'][0][3]
				s = parses[doc]['sentences'][sentenceOffSet]['parsetree']
				ptree = nltk.ParentedTree.fromstring(s)
				indices = [token[4] for token in relation['Connective']['TokenList']]
				clauses = pruning(ptree, indices)
				arg1 = relation['Arg1']['RawText']
				arg2 = relation['Arg2']['RawText']
				clauseExtractFeatures(clauses, relation['ConnectiveHead'], ptree, arg1, arg2)

	cPickle.dump(featureSet, open('SSFeatures.p','wb'))






