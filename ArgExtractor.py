import nltk
import json
import cPickle
import time

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

																																																																																									
def clauseProcessing(array):
	string = ' '.join(array)
	string = string.strip()
#
	punct = [' ...', ' ,', ' :', ' ;', ' ?', ' !', ' -', ' ~', ' .']
	for item in punct:
		while item in string:
			string = string.replace(item, item.strip())
#
	symbols = ['$ ', '# ', ' %']
	for item in symbols:
		while item in string:
			string = string.replace(item, item.strip())
#
	appos = [" 's", " n't", " 're"]
	for item in appos:
		while item in string:
			string = string.replace(item, item.strip())
#
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
#
	string = string.strip(',')
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


def rootpath(clause):
	path = ''
	while (clause.parent() != None):
		clause = clause.parent()
		path += clause.label()+'-'
	path = path.strip('-')
	return path


def height(phrase):
	i = 0
	try:
		while (phrase.parent().label() != ''):
			phrase = phrase.parent()
			i+=1
	except AttributeError:
		return i
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

def traverse(ptree):
	for child in ptree:
		if (type(child) != unicode):
			traverse(child)
			if child.label() in ['S', 'SBAR']:
				childLeaves = child.leaves()
				childString = clauseProcessing(childLeaves)
#
				global pos
				pos = []
				#clauseIndex(tree, child)
				#lca_loc = pos
				startIndex = 0
				for item in clauses:
					if (item[0] in childString):
						i = childString.index(item[0]) + len(item[0])
						if i>startIndex:
							startIndex = i
				print childString
				print startIndex
				print clauses
				print childString[startIndex:]
				if len(childString[startIndex:]) > 0:
					#print childString
					try:
						print 'before try'
						indices = getIndices(childString, startIndex, len(childString))
						lca_loc_1 = tree.leaf_treeposition(indices[0])
						lca_loc = lca(tree, indices)
						print lca_loc, startIndex
						print tree[lca_loc]
						if (type(tree[lca_loc]) != unicode):
							print 'IF TRUE'
							if (tree[lca_loc].label() != 'S'):
								lca_loc = lca_loc[:-1]
						print indices, lca_loc
						print 'after try'
					except UnboundLocalError:
						print 'before except'
						clauseIndex(tree, child)
						lca_loc_1 = lca_loc
						lca_loc_1.append(0)
						lca_loc_1 = tuple(lca_loc_1)
						lca_loc = tuple(pos)
						print 'after except'
					print 'CLAUSE APPEND ALERT!!!!!!!!!!!!!!!!!!!!!'
					print (childString[startIndex:], lca_loc)
					clauses.append((childString[startIndex:], lca_loc, lca_loc_1))
				else:
					clauseIndex(tree, child)
					lca_loc = tuple(pos)
#
				while (lca_loc != ()):
					lca_loc = lca_loc[:-1]
					parent = tree[lca_loc]
					if parent.label() in ['S', 'SBAR']:
						parentLeaves = parent.leaves()
						parentString = clauseProcessing(parentLeaves)
#
						index = parentString.index(childString)
						print childString
						print parentString
						if (index != 0):
							startIndex = 0
							for item in clauses:
								if (item[0] in parentString) and (item[0] not in childString):
									i = parentString.index(item[0]) + len(item[0])
									if i>startIndex:
										startIndex = i
							print parentString
							print childString
							print startIndex, index
							if (index >= startIndex):
								if (len(parentString[startIndex:index]) > 0):
									#print 'FULL STRING'
									#print parentString, startIndex, index
									indices = getIndices(parentString, startIndex, index)
									lca_loc_1 = tree.leaf_treeposition(indices[0])
									#print indices
									lca_loc = lca(tree, indices)
									print 'CLAUSE APPEND ALERT!!!!!!!!!!!!!!!!!!!!!'
									if (type(tree[lca_loc]) != unicode):
										print 'IF TRUE'
										if (tree[lca_loc].label() != 'S'):
											lca_loc = lca_loc[:-1]
									print (parentString[startIndex:index], lca_loc)
									clauses.insert(-1, (parentString[startIndex:index].strip(), lca_loc, lca_loc_1))
							else:
								print 'elseWHOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
								clauses.insert(-1, (parentString[:index].strip(), lca_loc))
						break
#	for item in clauses:
#		punctMarks = [',', ';', ':', '/', '?', '!', '~', '...']
#		treeString = clauseProcessing(tree.leaves())
#		for p in punctMarks:
#			if p in item[0]:
#				array = item[0].split(p)
#				for i in array:
#					index = treeString.index(i)
#					l = len(treeString[:index].split(' '))
#					indices = [x for x in range(l, l+len(i.strip().split(' ')))]
#					clauses.append((i.strip(), lca(tree, indices)))
				

def getIndices(childString, startIndex, index):
	punct = [',', ';', ':', '/', '?', '!', '~', '...', '$', '#', '%', "'s", "n't", "'re"]
	#print childString
	#print startIndex, index
	ptree = clauseProcessing(tree.leaves())
	ind = ptree.index(childString)
	k = ptree[:ind].strip().split(' ')
	if (k == ['']):
		k = 0
	else:
		k = len(k)
	for p in punct:
		i = -1
		while p in ptree[i+1:ind]:
			i += ptree[i+1:ind].index(p)+1
			k += 1
	l = childString[:startIndex].strip().split(' ')
	if (l == ['']):
		l = 0
	else:
		l = len(l)
	for p in punct:
		i = -1
		while p in childString[i+1:startIndex]:
			i += childString[i+1:startIndex].index(p)+1
			l += 1
	m = childString[startIndex:index].strip().split(' ')
	if (m == ['']):
		m = 0
	else:
		m = len(m)
	for p in punct:
		while p in childString[startIndex+1:index]:
			startIndex += childString[startIndex+1:index].index(p)+1
			m += 1
	indices = [x for x in range(k+l, k+l+m)]
	return indices


def clauseIndex(ptree, clause):
	global flag
	flag = False
	global pos
	pos = []
	for num, child in enumerate(ptree):
		if (child != clause) and (type(child) != unicode):
			#print child
			#time.sleep(2)
			clauseIndex(child, clause)
			#print flag
			if flag == True:
				pos.insert(0, num)
				print pos
				return
		elif (child == clause):
			pos.insert(0, num)
			flag = True
			return


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


	for num, item in enumerate(clauses):

		if (item[2] < lca_loc):
			clauseRelPosition = 'left'
		elif (item[2] > lca_loc):
			clauseRelPosition = 'right'
		else:
			clauses.pop(num)
			continue

		print clauses, num
		connString = clauseProcessing(connective.leaves())
		print item[0]
		print connString
		if (connString in item[0]):
			index = item[0].index(connString)
			item_1 = item[0][:index]
			item_2 = item[0][index+len(connString):]

		clause = tree[item[1]]
		if type(clause) == unicode:
			clause = tree[item[1][:-1]]

		if clause.left_sibling() != None:
			clauseLSPOS = clause.left_sibling().label()
		else:
			clauseLSPOS = 'NULL'
		if clause.right_sibling() != None:
			clauseRSPOS = clause.right_sibling().label()
		else:
			clauseRSPOS = 'NULL'

		clauseContext = clause.label()+'->'
		try:
			for child in clause:
				clauseContext += child.label() + '+'
				clauseContext.strip('+')
		except AttributeError:
			clauseContext = None

		conn2clausePath = path(connective, clause)

		conn2rootPath = rootpath(clause)

		featureVector = {'connectiveString':connHead, 'connectivePOS':connective.label(), 'leftSibNo':leftSibNo, 'rightSibNo':rightSibNo, 'connCategory':connCat, 'clauseRelPosition':clauseRelPosition, 'clauseContext':clauseContext, 'conn2clausePath':conn2clausePath, 'conn2rootPath':conn2rootPath}

		#leaves = clause.leaves()
		#clause = ' '.join(leaves)
		#punctuation = ['...', ',', ':', ';', '?', '!', '-', '~', '.']
		#for p in punctuation:
		#	if p in clause:
		#		index = clause.index(p)
		#		if clause[index-1] == ' ':
		#			clause = clause[:index-1]+clause[index:]
		#appos = ["'s", "n't"]
		#for item in appos:
		#	if item in clause:
		#		index = clause.index(item)
		#		if clause[index-1] == ' ':
		#			clause = clause[:index-1]+clause[index:]

		if item[0] in arg1:
			label = 'Arg1'
		elif item[0] in arg2:
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
			global tree
			tree = ptree
			indices = [token[4] for token in relation['Connective']['TokenList']]
			try:
				_clauses = traverse(tree)
				position = [item[2] for item in _clauses].sort()
				clauses = []
				for item in _clauses:
					for p in position:
						if item[2] == p:
							clauses.append(item[2])
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
				Arg1 = Arg1.strip(' ')
				Arg2 = Arg2.strip(' ')
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

	LabelsArg2=cPickle.load(open('LabelsArg2.p','r'))
	predictedLabelsArg2=cPickle.load(open('predictedLabelsArg2.p','r'))
	LabelsArg1=cPickle.load(open('LabelsArg1.p','r'))
	predictedLabelsArg1=cPickle.load(open('predictedLabelsArg1.p','r'))

	for num, item in enumerate(LabelsArg2):
	     if item != predictedLabelsArg2[num]:
		     print str(num)+'\t'+item+'\t'+predictedLabelsArg2[num]

	for num, item in enumerate(LabelsArg1):
	     if item != predictedLabelsArg1[num]:
		     print str(num)+'\t'+item+'\t'+predictedLabelsArg1[num]

