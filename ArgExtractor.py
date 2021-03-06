import nltk
import json
import cPickle
import sklearn
from conn_head_mapper import*
from confusion_matrix import*

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



def findHead(discourseBank):
	newdiscourseBank = discourseBank
	connectiveList=[]
	chm = ConnHeadMapper()
	for number,relation in enumerate(discourseBank):
		if relation['Type'] == 'Explicit':
			head, indices = chm.map_raw_connective(relation['Connective']['RawText'])
			discourseBank[number]['ConnectiveHead'] = head
	return discourseBank

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


def clauseExtractFeatures(clauses, connHead, indices):

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
		"""
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

		
		"""
		leaves = clause.leaves()
		clause = ' '.join(leaves)
		featureSet.append((featureVector, clause))
	return featureSet

	

def argsExtract(argClassifier,parsetree,indices):
	Arg2 = ''
	global ptree
	ptree=parsetree
	try:
		clauses = pruning(ptree, indices)
		c = ""
		for i in (indices):
	        	if i == 0:
	        		c = c + ptree[ptree.leaf_treeposition(i)]
        		else:
				c = c + " " + ptree[ptree.leaf_treeposition(i)]  
		chm = ConnHeadMapper()
		c=c.strip()
		connHead, ind = chm.map_raw_connective(c)	
		fSet = clauseExtractFeatures(clauses, connHead,indices)

		devFeatures = []
		tclauses = []
		for item in fSet:
			devFeatures.append(item[0])
			tclauses.append(item[1])
		l = argClassifier.classify_many(devFeatures)
		for num, label in enumerate(l):
			if label=='Arg2':
				Arg2 = Arg2+tclauses[num] + ' '
		Arg2 = Arg2.strip(' ')
		Arg2 = Arg2.strip(',')
		Arg2 = Arg2.strip(' ')
		#Arg2=Arg2.replace(' ,' , ',')
		#Arg2=Arg2.replace('`` ' , '"')
		Arg2=Arg2.replace('  ' , ' ')
		Arg2 = Arg2.strip(' ')

	except IndexError as e:
		print 'exceptions\n\n'
		#print ptree
		#print indices
	args={'arg2':Arg2}	
#	print args
	return args


if __name__ == "__main__":

        argClassifier = cPickle.load(open('PSarg2classifier.p', 'r'))

        devpdtb=[]
        f = open('dev-relations.json','r')
        for line in f:
                devpdtb.append(json.loads(line))
        f.close()

        devparses = json.loads(open('dev-parses.json','r').read())

	predictedLabelsArg2 = []
	LabelsArg2 = []

        predictedLabelsArg2string=[]
        LabelsArg2string=[]


	for relation in devpdtb:
		if (relation['Type'] == 'Explicit') and (relation['Arg1']['TokenList'][0][3] - relation['Arg2']['TokenList'][0][3] == -1):
			doc = relation['DocID']
			sentenceOffSet = relation['Arg2']['TokenList'][0][3]
			s = devparses[doc]['sentences'][sentenceOffSet]['parsetree']
			parsetree = nltk.ParentedTree.fromstring(s)
			leaf_index = [i[4] for i in relation['Connective']['TokenList']]
			argDict = argsExtract(argClassifier, parsetree, leaf_index)


            arg2string=argDict['arg2']
			arg2string=arg2string.replace(' ,',',')
			arg2string=arg2string.replace('`` ' , '"')

			while u" n't" in arg2string:
                                arg2string = arg2string.replace(" n't", "n't")

			while u" 's" in arg2string:
                                arg2string = arg2string.replace(" 's", "'s")

			predictedLabelsArg2string.append(arg2string)
			LabelsArg2string.append(relation['Arg2']['RawText'])

			arg2=[]
			leaves=parsetree.leaves()
			arg2words=argDict['arg2'].split()
			ind = -1

			string = ' '.join(leaves)
			ind = -1
			if ' '.join(arg2words[:2]) in string:
				ind = string.index(' '.join(arg2words[:2]))
				#print string[:ind].split()
				ind = len(string[:ind].split())-1
				if ind == 0:
					ind = -1

			arg2words=argDict['arg2'].split()
			for word in arg2words:
				ind += leaves[ind+1:].index(word)+1
				arg2.append(ind)

			predictedLabelsArg2.append(arg2)
			LabelsArg2.append([i[4] for i in relation['Arg2']['TokenList']])


#	print 'f1 arg2=',sklearn.metrics.f1_score( LabelsArg2,predictedLabelsArg2, average='micro')
#	print 'recall arg2=',sklearn.metrics.recall_score( LabelsArg2,predictedLabelsArg2, average='micro')
#	print 'precision arg2=',sklearn.metrics.precision_score( LabelsArg2,predictedLabelsArg2, average='micro')
	#print 'accuracy arg2=',sklearn.metrics.precision_score( LabelsArg2,predictedLabelsArg2)

	true_pos = 0
	false_neg = 0
	false_pos = 0
	true_neg = 0

	print 'Arg2 anomalies'
	true_pos = 0
	false_neg = 0
        for num, item in enumerate(LabelsArg2):
                if item	== predictedLabelsArg2[num]:
                        true_pos += 1
                else:
			if predictedLabelsArg2string[num] == LabelsArg2string[num]:
				predictedLabelsArg2string[num]
				print predictedLabelsArg2[num]
				print item, '\n\n'
                        false_neg += 1

	print true_pos
	print false_neg
