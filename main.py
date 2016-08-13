import json
import Classifiers
import cPickle as pickle
import nltk
import codecs
import ImplicitSenseFeatExtractor
import os
import xml.etree.ElementTree as ET

#connClassifier = nltk.classify.NaiveBayesClassifier.train(connFeatures)
#argPosClassifier= nltk.classify.NaiveBayesClassifier.train(argPosFeatures)
#argClassifier= nltk.classify.NaiveBayesClassifier.train(argFeatures)


class DiscourseParser(object):

	def __init__(self):
		pass

	def parse_file(self, input_file):
    connFeatures=pickle.load(open('connFeatures.p','r'))
    argPosFeatures=pickle.load(open('argPosFeatures.p','r'))
    senseFeatures=pickle.load(open('senseFeatures.p','r'))
    argFeatures = pickle.load(open('argFeatures.p','r'))
	  nonexplicitFeatures = cPickle.load(open('/home/f2012687/temp_SDP_master_codes/NonExplicitClassifierFeat.p', 'r'))
	  implicitsenseFeatures = cPickle.load(open('/home/f2012687/temp_SDP_master_codes/ImplicitSenseFeatExtractor.p', 'r'))
    connClassifier=nltk.MaxentClassifier.train(connFeatures)	
	  argPosClassifier= nltk.classify.MaxentClassifier.train(argPosFeatures)
    senseClassifier= nltk.classify.NaiveBayesClassifier.train(senseFeatures)
    argClassifier= nltk.classify.MaxentClassifier.train(argFeatures)
	  #nonexplicitClassifier = nltk.classify.MaxentClassifier.train(nonexplicitFeatures)
	  implicitsenseClassifier = nltk.classify.MaxentClassifier.train(implicitsenseFeatures)

	  pickle.dump(connClassifier, open('connClassifier.p','wb'))
	  pickle.dump(argPosClassifier, open('argPosClassifier.p','wb'))
	  pickle.dump(senseClassifier, open('senseClassifier.p','wb'))
	  pickle.dump(argClassifier, open('argClassifier.p','wb'))
	  #pickle.dump(nonexplicitClassifier, open('nonexplicitClassifier.p','wb'))
	  pickle.dump(implicitsenseClassifier, open('implicitsenseClassifier.p','wb'))

	  connClassifier = pickle.load(open('connClassifier.p','r'))        
	  argPosClassifier = pickle.load(open('argPosClassifier.p','r')) 
    PSarg1Classifier = pickle.load(open('PSarg1Classifier.p','r'))
	  senseClassifier = pickle.load(open('senseClassifier.p','r'))
	  argClassifier=pickle.load(open('kong_argClassifier.p','r'))
    #nonexplicitClassifier = pickle.load(open('nonexplicitClassifier.p','r'))
	  implicitsenseClassifier = pickle.load(open('implicitsenseClassifier_wo_parse_features.p','r'))

    documents = json.loads(codecs.open(input_file,mode='rb',encoding='utf-8').read())	
    relations = []
    for doc_id in documents:
      relations.extend(self.parse_doc(documents[doc_id], doc_id,connClassifier, argPosClassifier, senseClassifier,argClassifier, implicitsenseClassifier, PSarg1Classifier))
    return relations

	def parse_doc(self, doc, doc_id, connClassifier, argPosClassifier, senseClassifier, argClassifier, implicitsenseClassifier,PSarg1Classifier):
         store=0         
         output = []
         num_sentences = len(doc['sentences'])
         token_id = 0
         token_id_sentence=0
         for i in range(num_sentences):
              total=set(range(num_sentences))
              covered=set()
              uncovered=set()
              sentence1 = doc['sentences'][i]
              len_sentence1 = len(sentence1['words'])
              j=0
              while j < len_sentence1:
                  
                  wordString,connLabel,skip=Classifiers.classifyConnective(sentence1,j,connClassifier)       
                  if connLabel=='N' or connLabel == 'False':
                      token_id+=skip+1
                      j+=skip+1
                      continue
                  
                  argPosLabel,senseLabel,arg1List,arg2List=Classifiers.classifyOther(sentence1,wordString,j,skip,argPosClassifier,senseClassifier,argClassifier)
                  #print doc_id
                  if (argPosLabel=='PS' and i==0):
                      token_id+=skip+1
                      j+=skip+1
                      continue
                  try:
                      sentence2 = doc['sentences'][i-1]
                      len_sentence2 = len(sentence2['words'])
                      words = sentence2['words']
                  except IndexError:
                      store=i
                  covered.add(i) 
                  relation = {}
                  relation['DocID'] = doc_id
                  relation['Connective'] = {}
                  relation['Arg1'] = {}
                  relation['Arg2'] = {}

                  relation['Connective']['TokenList'] = range(token_id,token_id+skip+1)
                  relation['Type'] = 'Explicit'

                  if argPosLabel=='PS':

                      #relation['Arg1']['TokenList'] = range((token_id_sentence - len_sentence2), token_id_sentence - 1)
                      
                      #relation['Arg2']['TokenList'] = range(token_id_sentence, (token_id_sentence + len_sentence1) - 1)
                      arg1List = 3_ArgExtractor.arg(doc['sentences'][i-1]['parsetree'], wordString, PSarg1Classifier,doc['sentences'][i-1]['words'])
                      relation['Arg1']['TokenList'] = [i+token_id-j for i in arg1List]
                      #l = list(set(range(token_id-j, token_id -j + len_sentence1-1))-set([token_id]))
                      #l.sort()
                      #relation['Arg2']['TokenList'] =l
                      relation['Arg2']['TokenList'] = kong-finalPSArg2Extractor.argsExtract(PSarg2classifier,doc['sentences'][i-1]['parsetree'],relation['Connective']['TokenList'])
                  elif argPosLabel=='SS':
                      covered.add(i) 
                      relation['Arg1']['TokenList']=[i+token_id-j for i in arg1List] 
                      relation['Arg2']['TokenList']=[i+token_id-j for i in arg2List]
                    

                  relation['Sense'] = [senseLabel]
                  output.append(relation)
                  token_id += skip
                  token_id+=1
                  j+=skip+1
              token_id_sentence+=len_sentence1
           
         uncovered=list(total-covered)
         uncovered.sort()
         token_id=0	
	
	 featureSet = []
         for i in range(num_sentences-1):
             if i in uncovered:
                 sentence1 = doc['sentences'][i]
                 len_sentence1 = len(sentence1['words'])
                 token_id += len_sentence1
                 sentence2 = doc['sentences'][i+1]
                 len_sentence2 = len(sentence2['words'])
	         relation = {}
	         relation['Type'] = 'Implicit'
                 relation['DocID'] = doc_id
                 relation['Arg1'] = {}
                 relation['Arg1']['TokenList'] = range((token_id - len_sentence1), token_id - 1)
                 relation['Arg2'] = {}
       	         relation['Arg2']['TokenList'] = range(token_id, (token_id + len_sentence2) - 1)
		 print sentence1, sentence2, doc_id
		 feature = ImplicitClassifier2.extractFeatures(sentence1, sentence2, doc_id, model)
		 featureSet.append(feature)
		 senseType = implicitsenseClassifier.classify(feature)
		 print senseType
		 senseType = unicode(senseType)
	         relation['Sense'] = [senseType]
        	 relation['Connective'] = {}
               	 relation['Connective']['TokenList'] = []
	         output.append(relation)
	 f = pickle.dump(featureSet, open('implicitFeatureSet.p', 'wb'))
         return output
        

def getVerbNetClasses():
	verbNetClasses = {}
	for xmlfile in os.listdir('/home/manpreet/new_vn/'):
		if not xmlfile.endswith('.xml'):
			continue
		tree = ET.parse('/home/manpreet/new_vn/'+xmlfile)
		root = tree.getroot()
		#print root.attrib['ID']
		verbNetClasses[root.attrib['ID']] = []
		for mem in root.iter('MEMBER'):
			verbNetClasses[root.attrib['ID']].append(mem.attrib['name'])			
	return verbNetClasses


if __name__ == '__main__':
	#input_dataset = sys.argv[1]
	#input_run = sys.argv[2]
	#output_dir = sys.argv[3]
     global verbNetClasses
     global words
     global model
     model = gensim.models.Word2Vec.load_word2vec_format('/home/manpreet/word2vec/GoogleNews-vectors-negative300.bin', binary=True)
     parser = DiscourseParser()
     relations = parser.parse_file('/home/manpreet/dev-parses.json')
     output = open('output_dev.json', 'w')
     for relation in relations:
         output.write('%s\n' % json.dumps(relation))
     output.close()

