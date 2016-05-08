# Allen AI Science Challenge  
The Allen Institute for Artificial Intelligence (AI2) is working to improve humanity through fundamental advances in artificial intelligence.   
One critical but challenging problem in AI is to demonstrate the ability to consistently understand and correctly answer general questions about the world. 
Is your model smarter than an 8th grader? [Read More] (https://www.kaggle.com/c/the-allen-ai-science-challenge)  


## Question and Answer Pre-process
[question_answer_preprocess.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/question_answer_preprocess.py)  
### Question pre-process
- Remove punctuation 
- Convert to lowercase
- Part of speech tagging:  
Only use (nouns): [NN\*]  
Only use (noun, verb, adj/adv): [NN\* | VB\* | JJ\* | RB\*]  
- Concatenate question and each answer  

### Answer pre-process  
Replace:  
- `all of the above`: 16 in (2500 * 4 answers)  
(answer A + answer B + answer C)  
- `none of the above`: 4 in (2500 * 4 answers)  
(empty string)  
- `both A and B` & `both A and C`: 4 in (2500 * 4 answers)    
(answer A + answer B | answer C)  


## Knowledge Source
### Data collection
- CK12: 36 books & 6 subjects
- Study Cards: quizlet & studystack
- Simple wiki: simplewiki-20150702-pages-articles-multistream.xml [get_wiki_content.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/get_wiki_content.py)
- Aristo table: Nov 2015, Snapshot
- SuperSenseTagger: `to do: hyponymy & hypernymy query expansion`
- Google ngram: `to do: words distance` [get_google_dic.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/get_google_dic.py)

### Data cleaning
- CK12: [book title] -> [section title] -> [text] [clean_ck12.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/clean_ck12.py)
- Study Cards: [first notional word] -> [text] [clean_study_cards.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/clean_study_cards.py)
- Simple wiki: xml to text [clean_xml2text.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/clean_xml2text.py)
- Aristo table: `to do: data cleaning !`

## Ranking Algorithm
Support Vector Machine for Ranking: [SVMrank] (https://www.cs.cornell.edu/people/tj/svm_light/svm_rank.html)  
- Windows (32-bit)
- Use default setting `to do: optimize parameters`  
svm_rank_learn -c 20.0 train.dat model.dat  
svm_rank_classify ..\test.dat ..\model.dat ..\predictions  
- Prepare input data: [answer_ranking_features2txt.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/answer_ranking_features2txt.py)  
- Run SVMrank from Python: [answer_ranking_svmrank.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/answer_ranking_svmrank.py)

## Features 
- Retrieval Features [corpus_index_and_retrieval_feature.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/corpus_index_and_retrieval_feature.py)
- Word2vec Features  [w2v_feature.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/w2v_feature.py)
- Network Features: soft inference  [network_feature_index_retrieval_nodes.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/network_feature_index_retrieval_nodes.py) [network_feature.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/network_feature.py)
- Question Classification Features: soft inference 
  - Question Subjects [question_classification_subjects.py] (https://github.com/rarezhang/allen-ai-science-challenge/blob/master/src/question_classification_subjects.py)
  - Question Type 

### Retrieval Features
- Index  
Index corpuses separately: CK12 | Study Cards | Simple Wiki  
- 3 fields:  
  - Data source (book title) -> classification features
  - Document name (section title | first notional word) -> classification features
  - Content -> retrieval features
- Search: `to do: optimize parameters`  
StandardAnalyzer | hitsPerPage = 5 | DefaultSimilarity  
- 18 retrieval features   
![18 retrieval feature](https://cloud.githubusercontent.com/assets/5633774/14943834/95d85408-0f98-11e6-9d2b-7f010da47393.png "18 retrieval feature")

### Word2vec Features
- Training Word2Vec Model   
Train corpuses separately: CK12 | Study Cards
- Cosine similarity  
Each token in question V.S each token in each answer
- Only use noun 
- 4 word2vec features 
![4 word2vec features](https://cloud.githubusercontent.com/assets/5633774/14943861/374a4666-0f99-11e6-8bdc-dd7528c55a86.png "4 word2vec features")

### Network Features: soft inference 
- Based on [Random walk inference and learning in a large scale knowledge base] (https://www.cs.cmu.edu/~tom/pubs/lao-emnlp11.pdf)
- Modify and Simplify 
![difference](https://cloud.githubusercontent.com/assets/5633774/14943886/98794f86-0f99-11e6-872b-7d0de552f891.png "difference")
- Random walk probability  
![Random walk probability](https://cloud.githubusercontent.com/assets/5633774/14943903/105ab724-0f9a-11e6-9dc8-471a496cd69a.png "Random walk probability")
  - Path 1: Q -> 1 -> A
    - Degree(node1) = 4
    - ProbRandomWalkQ-A = 0.25
  - Path 2: Q -> 2 -> 3 -> A
    - Degree(node2) = 3  and  Degree(node3) = 3  
    - ProbRandomWalkQ-A = 0.11  
- Buid network (Based on Aristo table)
```to do: 1. Edges with attributes (e.g., 'absorb' -> edge attribute)  2. Undirected to directed graph``` 
  - plants -> absorb -> minerals
  - plants -> absorb -> nutrients  
![Buid network](https://cloud.githubusercontent.com/assets/5633774/14943919/9ab9feb6-0f9a-11e6-9382-fe87efc3152b.png "Buid network")
- Index
  - Nodes: text
  - Search: Each question V.S each answer
    - StandardAnalyzer | hitsPerPage = 1 | DefaultSimilarity
			`to do: optimize parameters`
- 13 network features  
![13 network features](https://cloud.githubusercontent.com/assets/5633774/14943962/896869ee-0f9b-11e6-970c-08b2a864cd9c.png "13 network features")

### Question Classification Features: soft inference
#### Classification Features - Subjects
- Question subjects (6 subjects): Biology | Physics | Earth Science | Life Science | Chemistry | Physical Science  
- Corpus: CK12 Textbooks
  - Compute the probability of all word wi  in the corpus appearing in the text of subject Sj: P(wi|Sj)
  - Sum the log P(wi|Sj) for all the words in the question and for all subjects   
![Question subjects](https://cloud.githubusercontent.com/assets/5633774/15100928/f2f4840c-1535-11e6-8953-3882a6b1f100.png "Question subjects")
- Index (3 fields)
  - Data source (book title) -> subjects classification 
  - Document name (section title) -> question type classification
  - Content
- Search  
text_query = QueryParser(version, 'text', analyzer).parse(QueryParser.escape(q_string))  
subject_query = QueryParser(version, 'corpus_name', analyzer).parse(QueryParser.escape(q_class))  
query = BooleanQuery()  
query.add(text_query, BooleanClause.Occur.SHOULD) #  the keyword SHOULD occur  
query.add(subject_query, BooleanClause.Occur.MUST) # the keyword MUST occur   
- 4 subjects classification features  
![4 subjects classification features](https://cloud.githubusercontent.com/assets/5633774/14943985/23679092-0f9c-11e6-894d-11b45f11c196.png " 4 subjects classification features")


#### Classification Features – Question type
- Question types (7 types):  Is-a |  Definition |  Property of objects |  Examples of situations |  Causality | Processes |  Domain specific models  
- Manually label 800 questions into 7 question types  
- Multi-class logistic regression classification with unigram-bigram features to classify the questions into 7 types
- Question types require inference  
  - Domain specific question
    - e.g., A boat is acted on by a river current flowing north and by wind blowing on its sails. The boat travels northeast. In which direction is the wind most likely applying force to the sails of the boat?
    - Abstraction 
  - Causality
    - e.g., What reason best explains why more people get colds in colder temperatures? 
    - Causal relation
  - Examples of situations
    - e.g., Which is an example of a chemical change? 
    - Instantiation

## Performance
- Training: allen-ai-training: 100001 - 101994  
- Testing: allen-ai-training: 101995 - 102500  

| Feature type  | Retrieval	| Word2vec	| Netowrk (2hops + 3hops)	| QuesClass(sub)|
| ------------- | ------------- | ------------- | ------------- | ------------- |
| P@1		|  53.95%	|  20.16%	|  20.95%	|  44.69%	|

| Features| Retrieval + Word2vec	| Retrieval + Word2vec + Netowrk(2hops + 3hops)| Retrieval + Word2vec + Netowrk(2hops + 3hops) + QuesClass(sub)|
| ------------- | ------------- | ------------- | ------------- | 
| P@1		|  56.13%	|  54.15%	|  55.34%	|  

| Corpus	| CK12		| Study Cards	| Simple wiki	|
| ------------- | ------------- | ------------- | ------------- | 
| P@1		|  47.04%	|  50.99%	|  39.33%	|  

- Training: allen-ai-training: 100001 - 102500  
- Testing: allen-ai-test: 102501 - 123798 

| Public Score	| Private Score	| 
| ------------- | ------------- | 
|  49.250%	|  50.285%	| 

### Performance - Network Features
Ni Lao 2011:  Random walk probability is useful as a feature in a combined ranking method, although not by itself a high precision feature 
- Network visualization: Entire network  
![Network visualization: Entire network](https://cloud.githubusercontent.com/assets/5633774/14944081/60d2cc74-0f9e-11e6-83d6-c4d49a097256.png " Network visualization: Entire network")
- Network visualization: Filter out degree <=1  
![Network visualization: Filter out degree <=1](https://cloud.githubusercontent.com/assets/5633774/14944116/0b65b35e-0f9f-11e6-886e-f2305e896f40.png " Network visualization: Filter out degree <=1")
- Modularity  
measure the strength of division of a network into modules  
![Modularity](https://cloud.githubusercontent.com/assets/5633774/14944109/e0294cfa-0f9e-11e6-9676-8997bfc197d9.png " Modularity")
- Zoom in to one module
  - According to Aristo table: `animals -> need -> sunligh` and `plants-> need -> sunlight`
  - According to Aristo table: `the sun -> hyponym -> important to all living things`
  - Soft inference: `Define living things: animals plants `
![Modularity](https://cloud.githubusercontent.com/assets/5633774/14944143/a0998414-0f9f-11e6-8353-496c91dfa74d.png " Modularity")
  - According to Aristo table: `the radiation -> heat -> from the sun`
  - According to Aristo table: `friction -> can -> cause heat`
  - Soft inference: `Heat source: radiation + friction`
![Modularity](https://cloud.githubusercontent.com/assets/5633774/14944160/37320a54-0fa0-11e6-9638-fbe328ca5ec1.png " Modularity")
```
to do  
  - Nodes (concepts): Data cleaning (no duplicates)  
  - Edges (relations): 
    - Combine with wordnet (hypernym | hyponym)
    - With attributes 
    - Noun <-> Noun
  - Need more `tables` (facts and relations extracted from textual data) 
  - Modularity: combine with question classification (subjects & question type )
```
