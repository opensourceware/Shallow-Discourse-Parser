import nltk
import json
import cPickle
import time
import sklearn
from helper import Helper
from conn_head_mapper import*
from confusion_matrix import*


class clauseExtractor:
	
	"""Takes parsetree of a sentence as input and returns clauses of the sentence."""

	def __init__(self, tree):
		self.tree = tree
		self._clauses = []

	def traverse(self, ptree):
		for child in ptree:
			if (type(child) != unicode):
				self.traverse(child)
				if child.label() in ['S', 'SBAR']:
					childLeaves = child.leaves()
					childString = self.clauseProcessing(childLeaves)
					childString = childString.strip('.')
					global pos
					pos = []
					startIndex = 0
					for item in self._clauses:
						if (item[0] in childString):
							i = childString.index(item[0]) + len(item[0])
							if i>startIndex:
								startIndex = i
					if len(childString[startIndex:]) > 0:
						try:
							indices = self.getIndices(childString, startIndex, len(childString))
							#lca_loc_1 is used to order the clauses
							lca_loc_1 = self.tree.leaf_treeposition(indices[0])
							lca_loc = Helper.lca(self.tree, indices)
							if (type(self.tree[lca_loc]) != unicode):
								if (self.tree[lca_loc].label() != 'S'):
									lca_loc = lca_loc[:-1]
						except UnboundLocalError:
							self.clauseIndex(self.tree, child)
							lca_loc_1 = lca_loc
							lca_loc_1.append(0)
							lca_loc_1 = tuple(lca_loc_1)
							lca_loc = tuple(pos)
						self._clauses.append((childString[startIndex:], lca_loc, lca_loc_1))
					else:
						self.clauseIndex(self.tree, child)
						lca_loc = tuple(pos)
					#Create clauses to the left of the childString and within the parent. The clauses to the right of childString
					#will be appended in the next recusion depth (current-1, since we are moving out of the recusion) where the 					
					#parent will be the childString.
					while (lca_loc != ()):
						lca_loc = lca_loc[:-1]
						parent = self.tree[lca_loc]
						if parent.label() in ['S', 'SBAR']:
							parentLeaves = parent.leaves()
							parentString = self.clauseProcessing(parentLeaves)
							if childString in parentString:
								index = parentString.index(childString)
							else:
								 index=0
							if (index != 0):
								startIndex = 0
								#certain substrings of parentString might already be a clause. This for loop searches
								#for that part of the substring which is not a part of any clause yet.
								for item in self._clauses:
									if (item[0] in parentString) and (item[0] not in childString):
										i = parentString.index(item[0]) + len(item[0])
										if i>startIndex:
											startIndex = i
								if (index >= startIndex):
									if (len(parentString[startIndex:index]) > 0):
										indices = self.getIndices(parentString, startIndex, index)
										if(indices!=[]):
											lca_loc_1 = self.tree.leaf_treeposition(indices[0])
											lca_loc = Helper.lca(self.tree, indices)
											if (type(self.tree[lca_loc]) != unicode):
												if (self.tree[lca_loc].label() != 'S'):
													lca_loc = lca_loc[:-1]
											self._clauses.insert(-1, (parentString[startIndex:index].strip(), lca_loc, lca_loc_1))
								else:
									self._clauses.insert(-1, (parentString[:index].strip(), lca_loc))

							break
		return self._clauses


	def getIndices(self, childString, startIndex, index):
		punct = [',', ';', ':', '/', '?', '!', '~', '...', '$', '#', '%', "'s", "n't", "'re"]
		ptree = self.clauseProcessing(self.tree.leaves())
		ind = ptree.index(childString)
		#k = number of words before childString starts
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
		#l = number of words between ind and startIndex
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
		#m = number of words between startIndex and index
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


	def clauseIndex(self, ptree, clause):
		global flag
		flag = False
		global pos
		pos = []
		for num, child in enumerate(ptree):
			if (child != clause) and (type(child) != unicode):
				self.clauseIndex(child, clause)
				if flag == True:
					pos.insert(0, num)
					return
			elif (child == clause):
				pos.insert(0, num)
				flag = True
				return

	def clauseProcessing(self, array):
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


class ClauseFeatExtractor:
	"""Extracts features of clauses of a sentence."""

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

	@classmethod
	def extractClauseFeatures(cls, clauses, connHead):
		features = []
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
			lca_loc = Helper.lca(ptree, indices)
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
		if connHead in cls.discourseAdverbial:
			connCat = 'Discourse Adverbial'
		elif connHead in cls.coordinatingConnective:
			connCat = 'Coordinating'
		elif connHead in cls.subordinatingConnective:
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
			connString = Helper.clauseProcessing(connective.leaves())
			clause = ptree[item[1]]
			if type(clause) == unicode or type(clause)== str:
				clause = ptree[item[1][:-1]]
			clauseContext = clause.label()+'->'
			try:
				for child in clause:
					clauseContext += child.label() + '+'
					clauseContext.strip('+')
			except AttributeError:
				clauseContext = None

			conn2clausePath = Helper.path(connective, clause)
			conn2rootPath = Helper.rootpath(clause)

			featureVector = {'connectiveString':connHead, 'connectivePOS':connective.label(), 'leftSibNo':leftSibNo, 'rightSibNo':rightSibNo, 'connCategory':connCat, 'clauseRelPosition':clauseRelPosition, 'clauseContext':clauseContext, 'conn2clausePath':conn2clausePath, 'conn2rootPath':conn2rootPath}

			if item[0] in arg1:
				label = 'Arg1'
			elif item[0] in arg2:
				label = 'Arg2'
			else:
				label = 'NULL'

			features.append((featureVector, item[0]))
		return features


class SSArgExtractor():
	"""Argument extractor for same sentence. The labels of this classifier are Arg1, Arg2 and None.
	This class inherits from ClauseFeatExtractor which provides the skeleton of feature engineering.
	SSArgExtractor and PSArgExtractor use the same features but provide different labels to its clauses."""
	
	featureSet = []

	def __init__(self, arg1, arg2):
		self.arg1 = arg1
		self.arg2 = arg2

	def extractClauseFeatures(self, clauses, connHead):
		features = ClauseFeatExtractor.extractClauseFeatures(clauses, connHead)
		for f in features:
			if f[1] in arg1:
				label = 'Arg1'
			elif f[1] in arg2:
				label = 'Arg2'
			else:
				label = 'NULL'
			SSArgExtractor.featureSet.append((f[0], label))


class PSArgExtractor():
	"""Argument extractor for same sentence. The labels of this classifier are Arg1, Arg2 and None.
	This class inherits from ClauseFeatExtractor which provides the skeleton of feature engineering.
	SSArgExtractor and PSArgExtractor use the same features but provide different labels to its clauses."""
	
	featureSet = []

	def __init__(self, arg2):
		self.arg2 = arg2

	def extractClauseFeatures(self, clauses, connHead):
		features = ClauseFeatExtractor.extractClauseFeatures(clauses, connHead)
		for f in features:
			if f[1] in arg2:
				label = 'Arg2'
			else:
				label = 'NULL'
			PSArgExtractor.featureSet.append((f[0], label))


if __name__ == "__main__":
	SStemp=0
	SStemp2=0
	PStemp=0
	PStemp2=0
	predictedLabelsArg1 = []
	LabelsArg1 = []
	predictedLabelsArg2 = []
	LabelsArg2 = []
	allFeat=[]
	
	pdtb = cPickle.load(open('pdtb.p', 'r'))
	pdtb = Helper.findHead(pdtb)
	parses = json.loads(open('pdtb-parses.json').read())
	for relation in pdtb:
		if (relation['Type'] == 'Explicit') and (relation['Arg1']['TokenList'][0][3] == relation['Arg2']['TokenList'][0][3]):
			doc = relation['DocID']
			sentenceOffSet = relation['Arg1']['TokenList'][0][3]
			s = parses[doc]['sentences'][sentenceOffSet]['parsetree']
			ptree = nltk.ParentedTree.fromstring(s)
			indices = [token[4] for token in relation['Connective']['TokenList']]
			SStemp2=SStemp2+1
			try:
				extr = clauseExtractor(ptree)
				_clauses = extr.traverse(ptree)
				position = [item[2] for item in _clauses]
				position.sort()
				#print 'position',position,'\n'
				clauses = []
				for p in position:
					for item in _clauses:
						if item[2] == p:
							clauses.append(item)
				#print clauses
				arg1 = relation['Arg1']['RawText']
				arg2 = relation['Arg2']['RawText']
				SSArgextr = SSArgExtractor(arg1, arg2)
				SSArgextr.extractClauseFeatures(clauses, relation['ConnectiveHead'])
			except IndexError as e:
				SStemp=SStemp+1
		elif (relation['Type'] == 'Explicit') and ((relation['Arg2']['TokenList'][0][3] - relation['Arg1']['TokenList'][0][3]) == 1):
			doc = relation['DocID']
			sentenceOffSet = relation['Arg1']['TokenList'][0][3]
			s = parses[doc]['sentences'][sentenceOffSet]['parsetree']
			ptree = nltk.ParentedTree.fromstring(s)
			indices = [token[4] for token in relation['Connective']['TokenList']]
			PStemp2=PStemp2+1
			try:
				extr = clauseExtractor(ptree)
				_clauses = extr.traverse(ptree)
				position = [item[2] for item in _clauses]
				position.sort()
				#print 'position',position,'\n'
				clauses = []
				for p in position:
					for item in _clauses:
						if item[2] == p:
							clauses.append(item)
				#print clauses
				arg1 = relation['Arg1']['RawText']
				arg2 = relation['Arg2']['RawText']
				PSArgextr = PSArgExtractor(arg2)
				PSArgextr.extractClauseFeatures(clauses, relation['ConnectiveHead'])
			except IndexError as e:
				PStemp=PStemp+1

	with open('SSargFeatures.p', 'wb') as f:
		cPickle.dump(SSArgextr.featureSet, f)
	f.close()

	with open('PSargFeatures.p', 'wb') as f1:
		cPickle.dump(PSArgextr.featureSet, f1)	
	f1.close()
	print 'temp count= ',SStemp, PStemp
	print 'temp2 count= ',SStemp2, PStemp2

