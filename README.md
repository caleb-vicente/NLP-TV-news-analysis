# NLP-TV news analysis
The development of the project is oriented to the extraction of topics and classification of written documents, obtained from subtitles of television broadcasts. For this purpose, we have experimented with different algorithms of word and document vectorization, topic modeling and clustering.
## Indroduction
In any problem related to data analysis (regardless of the data you have or the field of application), certain phases or processes must be fulfilled. Therefore, the project was divided into the following phases:

![alt text](https://github.com/caleb-vicente/NLP-TV-news-analysis/blob/main/img/stages_project.png)

- **Preparation**: During this phase, data will be extracted, selected and stored.
- **Preprocesado**: During preprocessing you want to prepare the data for further analysis. If an algorithm is well selected and works correctly, but the input data are not adequate, negative results will be obtained.
- **Análisis**: During the analysis stage, you will move from having simple collections of data to extracting information from them.
- **Postprocesado**: During this phase the information obtained from the analysis stage is evaluated. In this case TensorFlow Board, Matplotlib and PowerBI have been used as main tools.

## Models Used
The following algorithms have been used for the execution of the project (below you will find the bibliography of all the documentation used)

- **Vectorization algorithms:** Vectorization algorithms are nothing more than mechanisms capable of transforming text into feature vectors.
	- **One Hot Encoding:** Each vector of zeros will contain a single element of value one, characterizing the word in question.
	- **Words Embeddings: ** The main idea behind these algorithms is to reduce the dimension of the word representation.
		- **Word2Vec:** Algorithm self-supervised to represent similar words with closer vectors.
		- **TF-IDF:** The main idea is the multiplication of two different terms that provide complementary information.
- **Topic Modeling:**
	- **LSA:** It is based on the dimensionality reduction of the word-document matrix.
	- **LDA:** Allows to classify new documents without having to retrain with all the data again thanks to the generation of Dirichlet distributions.
	- **Doc2Vec:** Doc2Vec is a method of representing sentences or documents based on the ideas proposed in Word2Vec.
- **Clustering:**
	- **K-means:** Clustering algorithm by generating centroids and calculating Euclidean distances to them.

## Structure of the code
`pre` folder: Is in charge of both the reading of the documents containing the subtitles, as well as the information ingestion and preprocessing process.

`lda` folder: Training of the previously explained LDA algorithm.

`lsa` folder: Training of the altorithem LSA. TF-IDF applied to the original embeddings acted as the input of the algorithm.

`doc2vec` folder: Doc2Vec iplementation.

`classification` folder: Clustering implementation applied to the LSA, LDA and Doc2Vec algorithems.

`DBAdapter` folder: In the original application of the code, a database was used to store the original and processed data.
## Results

![alt text](https://github.com/caleb-vicente/NLP-TV-news-analysis/blob/main/img/topics.png)
Satisfactory topic results have been generated with sufficient words distance.

![alt text](https://github.com/caleb-vicente/NLP-TV-news-analysis/blob/main/img/topics_day.png)
There are specific days or weeks in which a special event occurs, in which a topic takes on greater importance. On the right we can see the temporal distribution of the topic "Independence of Catalonia" coinciding with the date on which the referendum was held in the region.

## Bibliography
[1] G. C. Tomas Mikolov Kai Chen y J. Dean, “Efficient Estimation of Word Repre-
sentations in Vector Space” https://arxiv.org/abs/1301.3781

[2] J. C. P. Dawn Chen y T. L. Griffiths, “Evaluating vector-space models of analogy” https://arxiv.org/abs/1705.04416

[3] A. Y. N. David M. Blei y M. I. Jordan, “Latent Dirichlet Allocation” https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf

[4] Q. Le y T. Mikolov, “Distributed Representations of Sentences and Documents” https://arxiv.org/pdf/1405.4053.pdf

[5] T. Hofmann, “Probabilistic Latent Semantic Analysis”, Proceedings of the Twenty-
Second Annual International SIGIR Conference on Research and Development in Information Retrieval (SIGIR-99) https://arxiv.org/abs/1301.6705
