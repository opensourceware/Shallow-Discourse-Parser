import nltk
import conn_head_mapper
import json
import cPickle
import codecs
import os
import FeatureExtractor
from nltk.stem.wordnet import WordNetLemmatizer
import xml.etree.ElementTree as ET


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


def lca(ptree,tokens):
    n = len(tokens)
    
    l=[ptree.leaf_treeposition(i) for i in tokens]
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


def root2leaf(ptree,location,i,flist):
    h = location.__len__()
    if i == h :
        return flist 
    else:
        flist.append(ptree[location[i]].label())
        ptree = ptree[location[i]]
        i+=1
        return root2leaf(ptree,location,i,flist)


def featureExtraction(discourseBank, treeBank):

	featureSet = []
	for relation in discourseBank:
        #print relation['DocID']
		if relation['Type']=='Explicit':
			connectiveString = relation['Connective']['RawText']
			connHead = relation['ConnectiveHead']
			indices = [index[4] for index in relation['Connective']['TokenList']]
			sentenceOffSet = relation['Connective']['TokenList'][0][3]
			doc=relation['DocID']

			tree=parses[doc]['sentences'][sentenceOffSet]['parsetree']
			ptree = nltk.ParentedTree.fromstring(tree)
			if ptree.leaves() != []:
				if len(indices) > 1:
					lca_loc = lca(ptree, indices)
				else:
					lca_loc = ptree.leaf_treeposition(indices[0])[:-1]
				connectivePOS = ptree[lca_loc].label()
				leftSibling = ptree[lca_loc].left_sibling()
				rightSibling = ptree[lca_loc].right_sibling()
				parentPOS = ptree[lca_loc].parent().label()
				if leftSibling == None:
					leftSiblingPOS = None
				else:
					leftSiblingPOS = leftSibling.label()
				if rightSibling == None:
					rightSiblingPOS = None
				else:
					rightSiblingPOS = rightSibling.label()

				if indices[0]==0:
					connectivePrev=None
				else:
					connectivePrev=parses[doc]['sentences'][sentenceOffSet]['words'][indices[0]-1][0]

				leaves = ptree.leaves()
				sentenceLen = len(leaves)
				m1 = sentenceLen*(1/3)
				m2 = sentenceLen*(2/3)
				if indices[len(indices)/2] < m1:
					cPosition = 'START'
				elif indices[len(indices)/2] >= m1 and indices[len(indices)/2] < m2:
					cPosition = 'MIDDLE'
				else:
					cPosition = 'END'

				flist = []
				r2l = root2leaf(ptree,lca_loc,0,flist)
				r2lcomp = r2l
				x=0
				while x < len(r2lcomp)-1 :
					if r2lcomp[x] == r2lcomp[x+1]:
						del r2lcomp[x+1]
					else:
						x += 1


	                if connHead in discourseAdverbial:
        	            connCat = 'Discourse Adverbial'
        	        elif connHead in coordinatingConnective:
        	            connCat = 'Coordinating'
        	        elif connHead in subordinatingConnective:
        	            connCat = 'Subordinating'
        	        else:
        	            connCat = None


	                subjectivityStrengthArg1 = 0
        	        subjectivityStrengthArg2 = 0
        	        arg1 = relation['Arg1']['RawText'].upper().split()
        	        arg2 = relation['Arg2']['RawText'].upper().split()
        	        for word in arg1:
        	            if word in subjectivity.keys():
        	                if subjectivity[word] == [u'negative', u'strongsubj']:
                	            subjectivityStrengthArg1 += -2
                        	if subjectivity[word] == [u'negative', u'weaksubj']:
                	            subjectivityStrengthArg1 += -1
                	        if subjectivity[word] == [u'positive', u'weaksubj']:
                        	    subjectivityStrengthArg1 += 1
                        	if subjectivity[word] == [u'negative', u'weaksubj']:
                        	    subjectivityStrengthArg1 += 2
                	for word in arg2:
                	    if word in subjectivity.keys():
                	        if subjectivity[word] == [u'negative', u'strongsubj']:
                	            subjectivityStrengthArg2 += -2
                	        if subjectivity[word] == [u'negative', u'weaksubj']:
                	            subjectivityStrengthArg2 += -1
                	        if subjectivity[word] == [u'positive', u'weaksubj']:
                	            subjectivityStrengthArg2 += 1
                	        if subjectivity[word] == [u'negative', u'weaksubj']:
                	            subjectivityStrengthArg2 += 2


			sentenceOffSetArg1 = relation['Arg1']['TokenList'][0][3]
			sentenceOffSetArg2 = relation['Arg2']['TokenList'][0][3]
			wordsArg1 = parses[doc]['sentences'][sentenceOffSetArg1]['words']
			wordsArg2 = parses[doc]['sentences'][sentenceOffSetArg2]['words']
			arg1indices = [item[4] for item in relation['Arg1']['TokenList']]
			arg2indices = [item[4] for item in relation['Arg2']['TokenList']]
			try:
				Arg1words = [wordsArg1[index] for index in arg1indices]
				Arg2words = [wordsArg2[index] for index in arg2indices]
			except IndexError:
				continue
#			fe = FeatureExtractor.FeatureExtractor()

			verbNetClassArg1 = verbNetClass(Arg1words)
			if verbNetClassArg1 == '':
				verbNetClassArg1 = None

			verbNetClassArg2 = verbNetClass(Arg2words)
			if verbNetClassArg2 == '':
				verbNetClassArg2 = None


                	featureVector={'Connective':connectiveString, 'connectiveHead': connHead, 'ConnectivePOS':connectivePOS, 'parentPOS':parentPOS, 'rightSiblingPOS':rightSiblingPOS, 'leftSiblingPOS':leftSiblingPOS, 'ConnectivePrev':connectivePrev, 'connectivePosition':cPosition, 'root2leaf':','.join(r2l), 'root2leafCompressed':','.join(r2lcomp), 'connectiveCategory':connCat, 'subjectivityStrengthArg1': subjectivityStrengthArg1, 'subjectivityStrengthArg2': subjectivityStrengthArg2, 'verbNetClassArg1': verbNetClassArg1, 'verbNetClassArg2': verbNetClassArg2}
			print featureVector
			featureLabel = relation['Sense'][0]
			featureSet.append((featureVector, featureLabel))   
	return featureSet


def verbNetClass(words):
	lemmatizer = WordNetLemmatizer()
	verb = ''
	verbClass = ''
	for word in words:
		label = word[1]['PartOfSpeech']
		if label in ['VB', 'VBD', 'VBG', 'VBP', 'VBZ']:
			if label == 'VB':
				verb = word[0]
				break
			elif (label in ['VBZ', 'VBP']):
				verb = word[0]
				verb = lemmatizer.lemmatize(verb, 'v')
			elif (label in ['VBD', 'VBG']):
				verb = word[0]
				verb = lemmatizer.lemmatize(verb, 'v')
	for item in verbNetClasses:
		if verb in verbNetClasses[item]:
			verbClass = item
	return verbClass


def getVerbNetClasses():
	verbNetClasses = {}
	for xmlfile in os.listdir('/home/manpreet/new_vn/'):
		if not xmlfile.endswith('.xml'):
			continue
		tree = ET.parse('/home/manpreet/new_vn/'+xmlfile)
		root = tree.getroot()
		print root.attrib['ID']
		verbNetClasses[root.attrib['ID']] = []
		for mem in root.iter('MEMBER'):
			verbNetClasses[root.attrib['ID']].append(mem.attrib['name'])			
	return verbNetClasses


if __name__=="__main__":

    pdtb = cPickle.load(open('dev.p','r'))
    parses = json.loads(open('dev-parses.json').read())    
    subjectivity = json.loads(open('mpqa_subj_05.json').read())
    verbNetClasses = getVerbNetClasses()

    featureSet=featureExtraction(pdtb, parses)
    cPickle.dump(featureSet, open('devExplicitFeatures.p','wb'))

#explicitFeatures=cPickle.load(open('ExplicitFeatures.p','rb'))
#devexplicitFeatures=cPickle.load(open('devExplicitFeatures.p','rb'))
#classifier = nltk.classify.NaiveBayesClassifier.train(explicitFeatures)
#print nltk.classify.accuracy(classifier, devexplicitFeatures)
