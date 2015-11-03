
featureSet = cPickle.load(open('featureSet.p','rb'))
labelSet = cPickle.load(open('labelSet.p','rb'))

trainSet=[]
for num, feature in enumerate(featureSet):
	trainSet.append((feature, labelSet[num][0]))

classifier = nltk.classify.NaiveBayesClassifier.train(trainSet)


