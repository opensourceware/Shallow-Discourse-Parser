#TODO:
#For the connectives labeled manually, make them case sensitive

import nltk, cPickle, json
parses = json.loads(open('pdtb-parses.json').read())

a = []

default = {
"as": {
		"as an alternative":"as an alternative",
		"as long as":"as long as",
		"as soon as":"as soon as",
		"insofar as":"insofar as",
		"largely as a result":"as a result", 
		"as":"as", 
		"as a result":"as a result",
		"as though":"as though",
		"as well":"as well", 
		"especially as":"as",
		"even as":"as", 
		"just as":"as",
		"just as soon as":"as soon as",
		"only as long as":"as long as",
		"particularly as":"as"
},

"by": {
		"by comparison":"by comparision",
		"by contrast":"by contrast",
		"by then":"by then"
},

"for": {
		"for":"for",
		"for example":"for example",
		"for instance":"for instance"
},

"in": {
		"in addition":"in addition",
		"in contrast":"in contrast",
		"in fact ":"in fact",
		"in other words":"in other words",
		"in particular":"in particular",
		"in short":"in short", 
		"in sum":"in sum", 
		"in the end":"in the end",
		"in turn":"in turn",
		"in the end":"in the end",
		"in contrast":"in contrast",
		"in start contrast":"in contrast",
		"in the mean time":"in the mean time"
},

"if": {
		"as if":"as if",
		"even if":"if",
		"if":"if",
		"if only":"if",
		"only if":"if",
		"when and if":"when and if",
		"if and when":"if and when",
		"especially if":"if",
		"particularly if":"if",
		"typically, if":"if"
},

"much": {
		"as much as":"much as",
		"much as":"much as",
		"so much as":"much as"
},

"on": {
		"on the contrary":"on the contrary",
		"on the one hand":"on the one hand",
		"on the other hand":"on the other hand"
},

"so": {
		"so":"so", 
		"so that":"so that"
},

"when": {
		"at least not when":"when",
		"back when":"when",
		"even when":"when",
		"at least when":"when",
		"especially when":"when",
		"except when":"when", 
		"just when":"when", 
		"only when":"when", 
		"particularly when":"when", 
		"usually when":"when",
		"when":"when",
}
}


def matchConnective(ptree, word, index):

	leaves = ptree.leaves()
	for num1, item in enumerate(leaves):
		leaves[num1] = item.lower()
	string = ' '.join(leaves)
	word = word.lower()
	connective = ''
	connectiveHead = ''
	if word in ['before','after', 'later']:
		lca_loc = ptree.leaf_treeposition(index)[:-1]
		leftSibling = ptree[lca_loc].left_sibling()
		if leftSibling != None:
			if (leftSibling.label() == 'RB') or (leftSibling.label() == 'ADVP'):
				preconnective = leftSibling.leaves()
				for n, item in enumerate(preconnective):
					preconnective[n] = item.lower()
				connective = ' '.join(preconnective)
			else:
				if index!=0:
					prevWord = leaves[index-1]
					lca_loc_prevWord = ptree.leaf_treeposition(index-1)[:-1]
					if prevWord in ['time', 'minute', 'minutes', 'year', 'years', 'day', 'days', 'week', 'weeks', 'month', 'months']:
						lca_loc_prevWordSiblings = lca_loc_prevWord[:-1]
						preconnective = ptree[lca_loc_prevWordSiblings].leaves()
						for n, item in enumerate(preconnective):
							preconnective[n] = item.lower()
						connective = ' '.join(preconnective)
		else:
			if index!=0:
				prevWord = leaves[index-1]
				lca_loc_prevWord = ptree.leaf_treeposition(index-1)[:-1]
				if prevWord in ['time', 'minute', 'minutes', 'year', 'years', 'day', 'days', 'week', 'weeks', 'month', 'months']:
					lca_loc_prevWordSiblings = lca_loc_prevWord[:-1]
					preconnective = ptree[lca_loc_prevWordSiblings].leaves()
					for n, item in enumerate(preconnective):
						preconnective[n] = item.lower()
					connective = ' '.join(preconnective)
		if connective == '':
			connective = word
		else:
			if word not in connective:
				connective = connective + ' ' + word
		if word == 'later':
			nextWord = leaves[index+1]
			if nextWord == 'on':
				connective += ' on'
		if connective.find(' ') != -1:
			pos = string.index(connective)
			if string[pos-4:pos-1] == ' in':
				connective = 'in ' + connective
			if string[pos-7:pos-1] == 'within':
				connective = 'within ' + connective
		connectiveHead = word


	elif word in ['afterward', 'afterwards', 'accordingly', 'additionally', 'also', 'alternatively', 'although', 'because', 'simultaneously', 'since', 'thereafter', 'until']:
		connective = ''
		lca_loc = ptree.leaf_treeposition(index)[:-1]
		leftSibling = ptree[lca_loc].left_sibling()
		if leftSibling != None:
			if leftSibling.label() == 'RB' or leftSibling.label() == 'ADVP':
				preconnective = leftSibling.leaves()
				for n, item in enumerate(preconnective):
					preconnective[n] = item.lower()
				connective = ' '.join(preconnective)
		if connective == '':
			connective = word
		else:
			connective += ' '+word
		if word == 'because':
			if connective.find(' ') != -1:
				pos = string.index(connective)
				prev = string[pos-14:pos-1]
				if prev == 'in large part':
					connective = prev + ' ' + connective
				prev = string[pos-8:pos-1]
				if prev == 'in part':
					connective = prev + ' ' + connective
		connectiveHead = word


	elif word in ['besides', 'but', 'consequently', 'conversely', 'earlier', 'else', 'except', 'finally', 'further', 'furthermore', 'hence', 'however', 'indeed', 'instead', 'lest', 'likewise', 'meantime', 'meanwhile', 'moreover', 'nevertheless', 'next', 'nonetheless', 'nor', 'once', 'or', 'otherwise', 'overall',  'plus', 'previously', 'rather', 'regardless', 'separately', 'similarly', 'specifically', 'still', 'then', 'thereby', 'therefore', 'though', 'thus', 'till', 'ultimately', 'unless', 'whereas', 'while', 'yet']:
		connective = ''
		connectiveHead = word
		if word == 'still':
			prevWord = leaves[index-1]
			if prevWord == 'even':
				connective = prevWord + ' ' + word
		if word == 'then':
			prevWord = leaves[index-1]
			if (prevWord == 'by') or (prevWord == 'even'):
				connective = prevWord + ' ' + word
		if word == 'though':
			prevWord = leaves[index-1]
			if (prevWord == 'even') or (prevWord == 'as'):
				connective = prevWord + ' ' + word
		if word == 'whereas':
			prevWord = leaves[index-1]
			if prevWord == 'even':
				connective = prevWord + ' ' + word
		if (word == 'meantime') or (word == 'meanwhile'):
			prevWord = leaves[index-1]+' '+leaves[index-2]
			if prevWord == 'in the':
				connective = prevWord + ' ' + word


	elif word in ['as', 'by', 'for', 'in', 'if', 'much', 'on', 'so', 'when']:
		possibleConnectives = []
		for item in default[word]:
			if (' '+item+' ') in string:
				possibleConnectives.append(item)
		l = [len(connective) for connective in possibleConnectives]
		try:
			connective = possibleConnectives[l.index(max(l))]
		except ValueError:
			return '', ''
		connectiveHead = default[word][connective]
		if word == 'if':
			if 'then' in leaves[leaves.index('if'):]:
				connective = 'if then'
				connectiveHead = 'if then'
				if (string.index('if') == 0):
					connective.capitalize()
		if connective == 'on the one hand':
			if 'on the other hand' in ' '.join(leaves):
				connective = "On the one hand On the other hand"
				connectiveHead = "on the one hand on the other hand"
			return connective, connectiveHead

	elif word == 'now':
		nextWord = leaves[leaves.index('now')+1]
		if nextWord == 'that':
			connective = 'now that'
			connectiveHead = 'now that'

	elif word == 'neither':
		if 'nor' in leaves[leaves.index('neither'):]:
			connective = 'neither nor'
			connectiveHead = 'neither nor'
			if (string.index('neither') == 0):
				connective = connective.capitalize()

	elif word == 'either':
		if 'or' in leaves[leaves.index('either'):]:
			connective = 'either or'
			connectiveHead = 'either or'
			if (string.index('either') == 0):
				connective = connective.capitalize()

	if connective != '':
		print connective
		print string
		if (connective == 'if then') or (connective == 'If then') or (connective == 'either or') or (connective == 'Either or') or (connective == 'neither nor') or (connective == 'Neither nor'):
			return connective, connectiveHead
		if (' ' not in connective) and (index==0):
			connective = connective.capitalize()
		elif (len(connective.split(' ')) > 1) and (string.index(connective) == 0):
			connective = connective.capitalize()
	return connective, connectiveHead

#with open('connective.p', 'a') as f:
#	for item in a:
#		f.write(item[0]+'\n')


