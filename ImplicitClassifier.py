import cPickle
import nltk

#labelSet=cPickle.load(open('/home/manpreet/implicit/TrainFeatures/labels.p','r'))
#featureSet = cPickle.load(open('/home/manpreet/implicit/TrainFeatures/implicitFeatures.p','r'))
featureSet = cPickle.load(open('ImplicitFeatures_noexp.p','rb'))
labelSet = cPickle.load(open('LabelSet_noexp.p','rb'))

#devFeatureSet = cPickle.load(open('/home/manpreet/implicit/DevFeatures/devImplicitFeatures.p','r'))
#devlabelSet=cPickle.load(open('/home/manpreet/implicit/DevFeatures/devLabelSet.p','r'))
devFeatureSet = cPickle.load(open('devImplicitFeatures_noexp.p','r'))
devlabelSet=cPickle.load(open('devLabelSet_noexp.p','r'))

trainSet=[]
for num, feature in enumerate(featureSet):
	trainSet.append((feature, labelSet[num][0]))

testSet=[]
ref = []
for num, feature in enumerate(devFeatureSet):
	ref.append(devLabelSet[num][0])
	testSet.append((feature, devLabelSet[num][0]))

classifier = nltk.classify.NaiveBayesClassifier.train(trainSet)
stage1 = classifier.classify_many(devFeatureSet)
print 'Stage1\t'+str(nltk.classify.accuracy(classifier, testSet))
print 'Stage1\t'+str(sklearn.metrics.f1_score(ref, stage1, average='weigthed'))

labels = classifier.labels()
for label in labels:
	trainSetStage2 = []
	for num, item in enumerate(labelSet):
		if item[0] == label:
			if len(item) > 1:
				trainSetStage2.append((featureSet[num], item[1]))
			else:
				trainSetStage2.append((featureSet[num], None))
	testSetStage2 = []
	devFeatureSetStage2 = []
	devLabelSetStage2 = []
	position = []
	for num, item in enumerate(stage1):
		if item == label:
			if len(item) > 1:
				position.append(num)
				devFeatureSetStage2.append(devFeatureSet[num])
				#devLabelSetStage2.append(devlabelSet[num][1])
				#testSetStage2.append((devFeatureSet[num], devlabelSet[num][1]))
			else:
				position.append(num)
				devFeatureSetStage2.append(devFeatureSet[num])
				#devLabelSetStage2.append(None)
				#testSetStage2.append((devFeatureSet[num], None))
	classifierStage2 = nltk.classify.NaiveBayesClassifier.train(trainSetStage2)
	stage2 = classifierStage2.classify_many(devFeatureSetStage2)
	labels2 = classifierStage2.labels()
	for num, item in enumerate(labels2):
		if item == None:
			labels2.pop(num)
	if (len(stage2) != len(position)):
		raise IndexError
	for num, pos in enumerate(position):
		if stage2[num] != None:
			stage1[pos] += '.'+stage2[num]
	#for num,item in enumerate(devLabelSetStage2):
	#	if item==None:
	#		devLabelSetStage2[num]=str(item)
	#for num,item in enumerate(stage2):
	#	if item==None:
	#		stage2[num]=str(item)
	#print 'Stage2\t'+label+'\t'+str(nltk.classify.accuracy(classifierStage2, testSetStage2))
	#try:
	#	print 'Stage2\t'+label+'\t'+str(sklearn.metrics.f1_score(devLabelSetStage2, stage2, average='weighted'))
	#except ValueError:
	#	continue
	for l in labels2:
		trainSetStage3 = []
		for num, item in enumerate(labelSet):
			try:
				if item[1] == l:
					if len(item) > 2:
						trainSetStage3.append((featureSet[num], item[2]))
					else:
						trainSetStage3.append((featureSet[num], None))
			except IndexError as e:
				pass
		testSetStage3 = []
		devFeatureSetStage3 = []
		devLabelSetStage3 = []
		position2 = []
		for num, item in enumerate(stage1):
			try:
				if item.split('.')[1] == l:
					if len(item) > 2:
						position2.append(num)
						devFeatureSetStage3.append(devFeatureSet[num])
						#devLabelSetStage3.append(item[2])
						#testSetStage3.append((devFeatureSet[num], item[2]))
					else:
						position2.append(num)
						devFeatureSetStage3.append(devFeatureSet[num])
						#devLabelSetStage3.append(None)
						#testSetStage3.append((devFeatureSet[num], None))
			except IndexError as e:
				pass
				#devLabelSetStage3.append(None)
				#testSetStage3.append((devFeatureSet[num], None))
		classifierStage3 = nltk.classify.NaiveBayesClassifier.train(trainSetStage3)
		stage3 = classifierStage3.classify_many(devFeatureSetStage3)
		labels3 = classifierStage3.labels()
		if (len(stage3) != len(position2)):
			raise IndexError
		for num, pos in enumerate(position2):
			if stage3[num] != None:
				stage1[pos] += '.'+stage3[num]
		#for num,item in enumerate(devLabelSetStage3):
		#	if item==None:
		#		devLabelSetStage3[num]=str(item)
		#for num,item in enumerate(stage3):
		#	if item==None:
		#		stage3[num]=str(item)
		#print 'Stage3\t'+l+'\t'+str(nltk.classify.accuracy(classifierStage3, testSetStage3))
		#try:
		#	print 'Stage3\t'+l+'\t'+str(sklearn.metrics.f1_score(devLabelSetStage3, stage3, average='weighted'))
		#except ValueError:
		#	continue



