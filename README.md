# Shallow-Discourse-Parser
Run the parser in following order:

1. python ConnectiveClassifier.py
2. python ArgumentPositionClassifier.py
3. python ArgFeatExtractor.py
4. python ExplicitSenseClassifier.py
5. python main.py
6. python tira_eval.py path_folder_having_given_relations.json_file path_folder_having_predicted_output.json_file path_folder_for_output

1-4 create feature files from training data;
5 runs parser on blind and test data (provided by CoNLL-Shared Task)
6 runs the evaluation script on the parser
