import nltk
import json
import cPickle
import time
import sklearn
from conn_head_mapper import*
from confusion_matrix import*


class Helper:

	"""Defines methods used recurrently by other classes."""
	@classmethod
	def findHead(cls, discourseBank):
		newdiscourseBank = discourseBank
		connectiveList=[]
		chm = ConnHeadMapper()
		for number,relation in enumerate(discourseBank):
			if relation['Type'] == 'Explicit':
				head, indices = chm.map_raw_connective(relation['Connective']['RawText'])
				discourseBank[number]['ConnectiveHead'] = head
		return discourseBank


	##this module joins elements of array by space and removes different charcter+space by only charcter return modified string
	@classmethod
	def lca(cls, ptree,leaf_index):
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


	@classmethod
	def rootpath(cls, clause):
		path = ''
		while (clause.parent() != None):
			clause = clause.parent()
			path += clause.label()+'-'
		path = path.strip('-')
		return path

	@classmethod
	def height(cls, phrase):
		i = 0
		try:
			while (phrase.parent().label() != ''):
				phrase = phrase.parent()
				i+=1
		except AttributeError:
			return i
		return i

	@classmethod
	def path(cls, conn, clause):
		if cls.height(conn) == cls.height(clause):
			return conn.label()+'U'+conn.parent().label()+'D'+clause.label()
		elif cls.height(conn) > cls.height(clause):
			distance = cls.height(conn)-cls.height(clause)+1
			p = conn.label()
			parent = conn
			while (distance != 0):
				parent = parent.parent()
				p += 'U'+parent.label()
				distance -= 1
			distance = cls.height(clause) - cls.height(parent)
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

	@classmethod
	def clauseProcessing(cls, array):
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

