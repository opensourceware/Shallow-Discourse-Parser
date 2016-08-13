import nltk, cPickle, json
import gensim
import nltk.data
from nltk.corpus import stopwords
import numpy as np
import gensim
import os, re
import xml.etree.ElementTree as ET
from conn_head_mapper import*
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from nltk.stem.wordnet import WordNetLemmatizer
#from confusion_matrix import*


def fscore_conf(classifier,testSet):
	conf_obj=ConfusionMatrix()
        true_label=[]
        predicted_label=[]
        for i in testSet:
        	true_label.append(i[1])
		predicted_label.append(classifier.classify(i[0]))
	conf_obj.add_list(predicted_label,true_label)
	conf_obj.print_matrix()
	f1_score=conf_obj.compute_average_f1()
	print 'F1 score = ',f1_score,'\n'	


def addProductionRules(ptree):
	childLabel=[]
	for child in ptree:
		if type(child) == unicode:
			return
		getproductionRules(child)
		childLabel.append(child.label())
	feature = (ptree.label(), tuple(childLabel))
	if feature in featureList:
		featureVector[feature] = True
	return


def addDependencyRules(dependencies):
	for rule in dependencies:
		dRule = rule[0]
		if rule[1][-1] < rule[2][-1]:
			orientation = 'right'
		else:
			orientation = 'left'
		feature = (dRule, orientation)
		if feature in featureList:
			featureVector[feature] = True


def addSubjectivityFeatures(arg1, arg2):
	subjectivityStrengthArg1 = 0
	subjectivityStrengthArg2 = 0
	for word in arg1:
		word = word.upper()
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
		word = word.upper()
		if word in subjectivity.keys():
			if subjectivity[word] == [u'negative', u'strongsubj']:
				subjectivityStrengthArg2 += -2
			if subjectivity[word] == [u'negative', u'weaksubj']:
				subjectivityStrengthArg2 += -1
			if subjectivity[word] == [u'positive', u'weaksubj']:
				subjectivityStrengthArg2 += 1
			if subjectivity[word] == [u'negative', u'weaksubj']:
				subjectivityStrengthArg2 += 2
	featureVector['subjectivityStrengthArg1'] = subjectivityStrengthArg1
	featureVector['subjectivityStrengthArg2'] = subjectivityStrengthArg2


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
	verbClasses = {}
	for xmlfile in os.listdir('/home/manpreet/new_vn/'):
		if not xmlfile.endswith('.xml'):
			continue
		tree = ET.parse('/home/manpreet/new_vn/'+xmlfile)
		root = tree.getroot()
		#print root.attrib['ID']
		verbClasses[root.attrib['ID']] = []
		for mem in root.iter('MEMBER'):
			verbClasses[root.attrib['ID']].append(mem.attrib['name'])			
	return verbClasses


def sentence_to_wordlist(text, remove_stopwords=False ):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    #
    # 1. Remove HTML
    #text = BeautifulSoup(review).get_text()
    #  
    # 2. Remove non-letters
    if text.startswith('.start'):
        text = text.strip('.start')
    text = re.sub("[^a-zA-Z ']"," ", text)
    #
    # 3. Convert words to lower case and split them
    text = text.lower()
    words = re.split(" |'", text)
    #print words
    try:
        if words[0] == '.start':
            words.pop(0)
    except IndexError as e:
        pass
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    #5. Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    words = [w for w in words if w != '']
    #6. Return a list of words
    return(words)


def addWord2VecFeatures(arg1, arg2, doc, model):
	vectorizer = TfidfVectorizer(analyzer='word', min_df = 2, stop_words = 'english', sublinear_tf=True)
	files = [f for f in os.listdir('/home/manpreet/train_raw')]
	files.sort()
	corpus = [open('/home/manpreet/train_raw/'+f, 'r').read() for f in files]

	for num,item in enumerate(corpus):
		try:
			corpus[num] = unicode(item)
		except UnicodeDecodeError as e:
			message = str(e)
			err_pos = int(message[message.index('position')+9:message.index(':')])
			corpus[num] = corpus[num][:err_pos]+corpus[num][err_pos+1:]

	for num,item in enumerate(corpus):
		try:
			corpus[num] = unicode(item)
		except UnicodeDecodeError as e:
			message = str(e)
			err_pos = int(message[message.index('position')+9:message.index(':')])
			corpus[num] = corpus[num][:err_pos]+corpus[num][err_pos+1:]

	for num, item in enumerate(corpus):
		words = sentence_to_wordlist(item)
		corpus[num] = ' '.join(words)

	weight_matrix = vectorizer.fit_transform(corpus)
	dense = weight_matrix.todense()
	feature_names = vectorizer.get_feature_names()
	numFeatures = len(feature_names)

	pcaArg1 = cPickle.load(open('pcaArg1.p', 'r'))
	pcaArg2 = cPickle.load(open('pcaArg2.p', 'r'))
	k_means_arg1 = cPickle.load(open('k_means_arg1.p', 'r'))
	k_means_arg2 = cPickle.load(open('k_means_arg2.p', 'r'))

	print arg1, arg2, doc
	num = int(doc[4:])-200
	arg1vector = [0.0001]*300
	arg2vector = [0.0001]*300
	arg1words = sentence_to_wordlist(arg1, remove_stopwords=True)
	arg2words = sentence_to_wordlist(arg2, remove_stopwords=True)
	for word in arg1words:
		arg1vector = iter(arg1vector)
		#c = [a.next()+b.next() for i in range(1,4)]
		try:
			loc = feature_names.index(word)
			tfidf = dense.item(numFeatures*num+loc)
			print word + ' ' + str(tfidf)
		except ValueError as e:
			continue
		try:
			#print word + ' ' + str(tfidf)
			b = iter(tfidf*model[word])
		except KeyError:
			continue
		arg1vector = [arg1vector.next()+b.next() for i in range(0, 300)]
	for word in arg2words:
		arg2vector = iter(arg2vector)
		try:
			loc = feature_names.index(word)
			tfidf = dense.item(numFeatures*num+loc)
			print word + ' ' + str(tfidf)
		except ValueError as e:
			continue
		try:
			#print word + ' ' + str(tfidf)
			b = iter(tfidf*model[word])
		except KeyError:
			continue
		arg2vector = [arg2vector.next()+b.next() for i in range(0, 300)]

	arg1list = list(arg1vector)
	arg2list = list(arg2vector)
	arg1vector = iter(arg1list)
	arg2vector = iter(arg2list)
	cosineDistance = 0.0
	for i in range(0, 300):
		cosineDistance += arg1vector.next()*arg2vector.next()

	featureVector['cosineDistance'] = cosineDistance

	arg1vector = arg1list
	arg2vector = arg2list
	arg1vector = np.array(arg1vector)
	arg2vector = np.array(arg2vector)
	arg1vector = pcaArg1.transform(arg1vector)
	arg2vector = pcaArg2.transform(arg2vector)
	Arg1Cluster = k_means_arg1.predict(arg1vector)
	Arg2Cluster = k_means_arg2.predict(arg2vector)
	featureVector['Arg1Cluster'] = list(Arg1Cluster)[0]
	featureVector['Arg2Cluster'] = list(Arg1Cluster)[0]


def extractFeatures(sentence1, sentence2, doc, model):

#	global feature_names
#	global numFeatures
#	global dense
#	global pcaArg1
#	global pcaArg2
#	global k_means_arg1
#	global k_means_arg2
#
	global featureVector
	global subjectivity
	global featureList
	global verbNetClasses
	verbNetClasses = getVerbNetClasses()
        subjectivity = json.loads(open('/home/manpreet/mpqa_subj_05.json').read())
        featureList = cPickle.loads(open('/home/manpreet/featureList.p', 'r').read())
	featureVector = {}
	
	for feature in featureList:
		featureVector[feature] = False

	parsetree1 = sentence1['parsetree']
	addProductionRules(parsetree1)
	dependencies1 = sentence1['dependencies']
	addDependencyRules(dependencies1)

	parsetree2 = sentence2['parsetree']
	addProductionRules(parsetree2)
	dependencies2 = sentence2['dependencies']
	addDependencyRules(dependencies2)

	words1 = [word[0] for word in sentence1['words']]
	words2 = [word[0] for word in sentence2['words']]
	addSubjectivityFeatures(words1, words2)

	verbNetClassArg1 = verbNetClass(sentence1['words'])
	if verbNetClassArg1 == '':
		verbNetClassArg1 = None
	featureVector['verbNetClassArg1'] = verbNetClassArg1

	verbNetClassArg2 = verbNetClass(sentence2['words'])
	if verbNetClassArg2 == '':
		verbNetClassArg2 = None
	featureVector['verbNetClassArg2'] = verbNetClassArg2

	addWord2VecFeatures(' '.join(words1), ' '.join(words2), doc, model)

	#return featureVector


if __name__ == "__main__":

	global verbNetClasses
	verbNetClasses = getVerbNetClasses()

        featureList = cPickle.loads(open('/home/manpreet/featureList.p', 'r').read())

        model = gensim.models.Word2Vec.load_word2vec_format('/home/manpreet/word2vec/GoogleNews-vectors-negative300.bin', binary=True)
        subjectivity = json.loads(open('/home/manpreet/mpqa_subj_05.json').read())

        #trainfeatureSet = cPickle.load(open('ImplicitSenseFeatures_wo_parse_features.p','r'))
#        classifier = cPickle.load(open('implicitsenseClassifier_wo_parse_features.p', 'r'))

#        devpdtb=[]
#        f = open('/home/f2012687/dev-relations.json','r')
#        for line in f:
#                devpdtb.append(json.loads(line))
#        f.close()

	vectorizer = TfidfVectorizer(analyzer='word', min_df = 2, stop_words = 'english', sublinear_tf=True)
	files = [f for f in os.listdir('/home/manpreet/train_raw')]
	files.sort()
	corpus = [open('/home/manpreet/train_raw/'+f, 'r').read() for f in files]

	for num,item in enumerate(corpus):
		try:
			corpus[num] = unicode(item)
		except UnicodeDecodeError as e:
			message = str(e)
			err_pos = int(message[message.index('position')+9:message.index(':')])
			corpus[num] = corpus[num][:err_pos]+corpus[num][err_pos+1:]

	for num,item in enumerate(corpus):
		try:
			corpus[num] = unicode(item)
		except UnicodeDecodeError as e:
			message = str(e)
			err_pos = int(message[message.index('position')+9:message.index(':')])
			corpus[num] = corpus[num][:err_pos]+corpus[num][err_pos+1:]

	for num, item in enumerate(corpus):
		words = sentence_to_wordlist(item)
		corpus[num] = ' '.join(words)

	weight_matrix = vectorizer.fit_transform(corpus)
	dense = weight_matrix.todense()
	feature_names = vectorizer.get_feature_names()
	numFeatures = len(feature_names)

	pcaArg1 = cPickle.load(open('pcaArg1.p', 'r'))
	pcaArg2 = cPickle.load(open('pcaArg2.p', 'r'))
	k_means_arg1 = cPickle.load(open('k_means_arg1.p', 'r'))
	k_means_arg2 = cPickle.load(open('k_means_arg2.p', 'r'))

	pdtb = cPickle.load(open('/home/manpreet/dev-pdtb.p', 'r'))
        parses = json.loads(open('/home/manpreet/dev-parses.json','r').read())

        featureSet = []
        label = 'None'
        for rel in pdtb:
                if (rel['Type'] == u'Implicit'):
                        label = rel['Sense'][0]
                       	doc = rel['DocID']
                        arg1sentenceOffSet = rel['Arg1']['TokenList'][0][3]
                        sentence1 = parses[doc]['sentences'][arg1sentenceOffSet]
                        arg2sentenceOffSet = rel['Arg2']['TokenList'][0][3]
                       	sentence2 = parses[doc]['sentences'][arg2sentenceOffSet]
                        featureVector = {}
                       	extractFeatures(sentence1, sentence2, doc)
                       	print label
                        if label != 'None':
                                featureSet.append((featureVector, label))

        cPickle.dump(featureSet, open('senseFeatureSet1.p', 'w'))
#        print '......................................ON DEVELOPMENT DATA..................','\n'

#        fscore_conf(classifier, devfeatureSet)
#        print 'Accuracy = ',nltk.classify.accuracy(classifier, devfeatureSet),'\n'

