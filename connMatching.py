#TODO:
#For the connectives labeled manually, make them case sensitive

import nltk, cPickle, json
parses = json.loads(open('pdtb-parses.json').read())

a = []

default = {
"as": {
		"as an alternative":"as an alternative",
		"as if":"as if",
		"as long as":"as long as",
		"much as":"much as",
		"as soon as":"as soon as",
		"as well":"as well",
		"insofar as":"insofar as",
		"largely as a result":"as a result", 
		"as":"as", 
		"as a result":"as a result",
		"as long as":"as long as", 
		"as much as":"much as",
		"as though":"as though",
		"as well":"as well", 
		"especially as":"as",
		"even as":"as", 
		"just as":"as",
		"just as soon as":"as soon as",
		"much as":"much as",
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
		"for instance":"for instance":
},

"in": {
		"in addition":"in addition",
		"in contrast":"in contrast",
		"in fact":"in fact",
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
		"even if":"even if",
		"if":"if",
		"if only":"if",
		"when and if":"when and if",
		"as if":"as if",
		"especially if":"if",
		"particularly if":"if",
		"even if":"if",
		"if and when":"if and when",
		"only if":"if",
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
		"just when":"when",
		"only when":"when",
		"at least when":"when",
		"especially when":"when",
		"even when":"when",
		"except when":"when", 
		"just when":"when", 
		"only when":"when", 
		"particularly when":"when", 
		"usually when":"when",
		"when":"when",
}
}





for doc in parses:
	for sentence in parses[doc]['sentences']:
		ptree = nltk.ParentedTree.fromstring(sentence['parsetree'])
		leaves = ptree.leaves()
		string = ' '.join(leaves)
		for num1, item in enumerate(leaves):
			leaves[num1] = item.lower()
		for word in leaves:
			connective = ''
			if word in ['before','after', 'later']:
				try:
					index = leaves.index(word)
				except ValueError:
					break
				lca_loc = ptree.leaf_treeposition(index)[:-1]
				leftSibling = ptree[lca_loc].left_sibling()
				if leftSibling != None:
					if (leftSibling.label() == 'RB') or (leftSibling.label() == 'ADVP'):
						preconnective = leftSibling.leaves()
						connective = ' '.join(preconnective)
					else:
						if index!=0:
							prevWord = leaves[index-1]
							lca_loc_prevWord = ptree.leaf_treeposition(index-1)[:-1]
							if prevWord in ['time', 'minute', 'minutes', 'year', 'years', 'day', 'days', 'week', 'weeks', 'month', 'months']:
								lca_loc_prevWordSiblings = lca_loc_prevWord[:-1]
								preconnective = ptree[lca_loc_prevWordSiblings].leaves()
								connective = ' '.join(preconnective)
				else:
					if index!=0:
						prevWord = leaves[index-1]
						lca_loc_prevWord = ptree.leaf_treeposition(index-1)[:-1]
						if prevWord in ['time', 'minute', 'minutes', 'year', 'years', 'day', 'days', 'week', 'weeks', 'month', 'months']:
							lca_loc_prevWordSiblings = lca_loc_prevWord[:-1]
							preconnective = ptree[lca_loc_prevWordSiblings].leaves()
							connective = ' '.join(preconnective)
				if connective == '':
					connective = word
				else:
					connective = connective + ' ' + word
				if word == 'later':
					nextWord = leaves[index+1]
					if nextWord == 'on':
						connective += ' on'
				if connective.find(' ') != -1:
					firstWord = connective[:connective.find(' ')]
					prevWord = leaves[leaves.index(firstWord.lower())-1]
					if prevWord == 'in':
						connective = 'in ' + connective
				connectiveHead = word


			elif word in ['afterward', 'afterwards', 'accordingly', 'additionally', 'also', 'alternatively', 'although', 'because', 'simultaneously', 'since', 'thereafter', 'until']:
				connective = ''
				try:
					index = leaves.index(word)
				except ValueError:
					break
				lca_loc = ptree.leaf_treeposition(index)[:-1]
				leftSibling = ptree[lca_loc].left_sibling()
				if leftSibling != None:
					if leftSibling.label() == 'RB' or leftSibling.label() == 'ADVP':
						preconnective = leftSibling.leaves()
						connective = ' '.join(preconnective)
				if connective == '':
					connective = word
				else:
					connective += ' '+word
				if word == 'because':
					if connective.find(' ') != -1:
						firstWord = connective[:connective.find(' ')]
						prevWord = leaves[leaves.index(firstWord.lower())-1]
						if prevWord == 'in':
							connective = 'in ' + connective
				connectiveHead = word


			elif word in ['besides', 'but', 'consequently', 'conversely', 'earlier', 'else', 'except', 'finally', 'further', 'furthermore', 'hence', 'however', 'indeed', 'instead', 'lest', 'likewise', 'meantime', 'meanwhile', 'moreover', 'nevertheless', 'next', 'nonetheless', 'nor', 'once', 'or', 'otherwise', 'overall',  'plus', 'previously', 'rather', 'regardless', 'separately', 'similarly', 'specifically', 'still', 'then', 'thereby', 'therefore', 'though', 'thus', 'till', 'ultimately', 'unless', 'whereas', 'while', 'yet']:
				connective = ''
				connectiveHead = word
				try:
					index = leaves.index(word)
				except ValueError:
					break
				if word == 'still':
					prevWord = leaves[index-1]
					if prevWord == 'even':
						word = prevWord + ' ' + word
				if word == 'then':
					prevWord = leaves[index-1]
					if (prevWord == 'by') or (prevWord == 'even'):
						word = prevWord + ' ' + word
				if word == 'though':
					prevWord = leaves[index-1]
					if (prevWord == 'even') or (prevWord == 'as'):
						word = prevWord + ' ' + word
				if word == 'whereas':
					prevWord = leaves[index-1]
					if prevWord == 'even':
						word = prevWord + ' ' + word
				if (word == 'meantime') or (word == 'meanwhile'):
					prevWord = leaves[index-1]+' '+leaves[index-2]
					if prevWord == 'in the':
						word = prevWord + ' ' + word
				connective = word


			elif word in ['as', 'by', 'for', 'in', 'if', 'much', 'on', 'so', 'when']:
				possibleConnectives = []
				for item in default[word]:
					if item in string:
						possibleConnectives.append(item)
				l = [len(connective) for connective in possibleConnectives]
				try:
					connective = possibleConnectives[l.index(max(l))]
				except ValueError:
					pass
				connectiveHead = default[word][connective]
				if word == 'if':
					if 'then' in leaves[leaves.index('if'):]:
						connective = 'if then'
						connectiveHead = 'if then'
				if connective == 'on the one hand':
					if 'on the other hand' in ' '.join(leaves):
						connective = "On the one hand On the other hand"
						connectiveHead = "on the one hand on the other hand"

			elif word == 'insofar':
				nextWord = leaves[leaves.index('insofar')+1]
				if nextWord == 'as':
					connective = 'insofar as'
					connectiveHead = 'insofar as'

			elif word == 'now':
				nextWord = leaves[leaves.index('now')+1]
				if nextWord == 'that':
					connective = 'now that'
					connectiveHead = 'now that'

			elif word == 'neither':
				if 'nor' in leaves[leaves.index('neither'):]:
					connective = 'neither nor'
					connectiveHead = 'neither nor'

			elif word == 'either':
				if 'or' in leaves[leaves.index('either'):]:
					connective = 'either or'
					connectiveHead = 'either or'

			

			if connective != '':
				a.append((connective, ptree, sentence['dependencies']))

with open('connective.p', 'a') as f:
	for item in a:
		f.write(item[0]+'\n')


