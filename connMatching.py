import nltk, cPickle, json
parses = json.loads(open('pdtb-parses.json').read())

a = []

default = {
"as": [
		"as an alternative", 
		"as if", 
		"as long as", 
		"much as", 
		"as soon as",
		"as well", 
		"insofar as", 
		"largely as a result", 
		"as", 
		"as a result",  
		"as long as", 
		"as much as",
		"as though",
		"as well" 
		"especially as",
		"even as", 
		"just as",
		"just as soon as",
		"much as",
		"only as long as",
		"particularly as",
		"so much as"
],

"by": [
		"by comparison", 
		"by contrast", 
		"by then"
],

"for": [
		"for", 
		"for example",
		"for instance"
],

"in": [
		"in addition", 
		"in contrast", 
		"in fact", 
		"in other words", 
		"in particular", 
		"in short", 
		"in sum", 
		"in the end",
		"in the meantime", 
		"in the meanwhile",
		"in turn",
		"in the end",
		"in contrast",
		"in start contrast",
		"in the mean time"
],

"if": [
		"as if",
		"even if",
		"if",
		"if only",
		"if then",
		"when and if",
		"as if",
		"especially if",
		"particularly if",
		"even if",
		"if and when",
		"only if",
		"typically, if"
],

"much": [
		"as much as",
		"much as",
		"so much as"
],

"on": [
		"on the contrary", 
		"on the one hand", 
		"on the other hand", 
],

"so": [
		"so", 
		"so that"
],

"when": [
		"at least not when", 
		"back when", 
		"even when", 
		"just when", 
		"only when",
		"at least when", 
		"especially when", 
		"even when",
		"except when", 
		"just when", 
		"only when", 
		"particularly when", 
		"usually when",
		"when",
]
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


			elif word in ['afterward', 'accordingly', 'additionally', 'also', 'alternatively', 'although', 'because', 'simultaneously', 'since', 'thereafter', 'until']:
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


			elif word in ['besides', 'but', 'consequently', 'conversely', 'earlier', 'else', 'except', 'finally', 'further', 'furthermore', 'hence', 'however', 'indeed', 'instead', 'lest', 'likewise', 'meantime', 'meanwhile', 'moreover', 'nevertheless', 'next', 'nonetheless', 'nor', 'once', 'or', 'otherwise', 'overall',  'plus', 'previously', 'rather', 'regardless', 'separately', 'similarly', 'specifically', 'still', 'then', 'thereby', 'therefore', 'though', 'thus', 'till', 'ultimately', 'unless', 'whereas', 'while', 'yet']:
				connective = ''
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

			elif word == 'either':
				nextWord = leaves[leaves.index('either')+1]
				if nextWord == 'or':
					connective = 'either or'

			elif word == 'insofar':
				nextWord = leaves[leaves.index('insofar')+1]
				if nextWord == 'as':
					connective = 'insofar as'

			elif word == 'neither':
				nextWord = leaves[leaves.index('neither')+1]
				if nextWord == 'nor':
					connective = 'neither nor'

			elif word == 'now':
				nextWord = leaves[leaves.index('now')+1]
				if nextWord == 'that':
					connective = 'neither nor'
			if connective != '':
				a.append((connective, ptree, sentence['dependencies']))

with open('connective.p', 'a') as f:
	for item in a:
		f.write(item[0]+'\n')


