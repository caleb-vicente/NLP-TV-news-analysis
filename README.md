# NLP-TV news analysis
El desarrollo del proyecto está orientado a la extracción de temas y clasificación de documentos escritos, obtenidos a partir de subtítulos de emisiones televisivas. Para ello, se ha experimentado con diferentes algoritmos de vectorización de palabras y documentos, topic modeling y clustering.
## Indroduction
En cualquier problema relacionado con el análisis de datos (independientemente de los datos que se tengan o el campo de aplicación), se deben cumplir ciertas fases o procesos. Por tanto, el proyecto se dividió en las siguientes fases:

![alt text](https://github.com/caleb-vicente/NLP-TV-news-analysis/blob/main/img/stages_project.png)

- **Preparación**: Durante esta fase se realizará desde la extracción de los datos, hasta la selección y almacenamiento de los mismos.
- **Preprocesado**: Durante el preprocesado se desea preparar los datos para su posterior analysis. Si un algoritmo está bien seleccionado y funciona de manera correcta, pero los datos que se le introducen como entrada no son los adecuados, se obtendrán resultados negativos.
- **Análisis**: Durante la etapa del análisis se pasará de tener simples colecciones de datos a extraer información de las mismos.
- **Postprocesado**: Durante esta fase se evalúa la información obtenida a partir de la etapa de análisis. En este caso se ha usado TensorFlow Board, Matplotlib y PowerBI como princpipales herramientas.

## Models Used
Para la ejecución del proyecto se han usado los siguientes algoritmos. (Más abajo podrá encontrar la bibliografía de toda la documentación utilizada)

- **Vectorization algorithms:** Los algoritmos de vectorización, no son más que mecanismos capaces de transformar texto en vectores de características.
	- **One Hot Encoding:** Cada vector de ceros contendrá un único elemento de valor uno, caracterizando la palabra en cuestión.
	- **Words Embeddings: ** The main idea behind these algorithms is to reduce the dimension of the word representation.
		- **Word2Vec:** Algorithm self-supervised to represent similar words with closer vectors.
		- **TF-IDF:** La idea principal es la multiplicación de dos términos distintos que aportan información complementaria.
- **Topic Modeling:**
	- **LSA:** Se basa en la reducción de dimensionalidad de la matriz palabras-documentos.
	- **LDA:** Permite clasificar nuevos documentos sin tener que reentrenar con todos los datos de nuevo gracias a las generación de distribuciones de Dirichlet
	- **Doc2Vec:** Doc2Vec es un método de representación de oraciones o documentos basado en las ideas propuestas en Word2Vec
- **Clustering:**
	- **K-means:** Algoritmo de clustering mediante la generación de centroides y calculo de distancias euclidias a los mismos.

## Structure of the code
`pre` folder: se encarga tanto de la lectura de los documentos que contienen los subtítulos, así como el proceso de ingesta y preprocesado de información.

`lda` folder: Entrenamiento del algoritmo LDA previamente explicado.

`lsa` folder: Entrenamiento del algoritmo LSA. Como entrada del algoritmo se ha aplicado TF-IDF a los embeddings originales.

`doc2vec` folder: Aplicación de Doc2Vec.

`classification` folder: Aplicación de clustering a los datos de salida de los algoritmos lda, lsa o doc2vec.

`DBAdapter` folder: En la aplicación original del código se usó una base de datos para guardar los datos originales y los procesados.

## Results

https://github.com/caleb-vicente/NLP-TV-news-analysis/blob/main/img/topics.png

https://github.com/caleb-vicente/NLP-TV-news-analysis/blob/main/img/topics_day.png

## Bibliography
[1] G. C. Tomas Mikolov Kai Chen y J. Dean, “Efficient Estimation of Word Repre-
sentations in Vector Space” https://arxiv.org/abs/1301.3781

[2] J. C. P. Dawn Chen y T. L. Griffiths, “Evaluating vector-space models of analogy” https://arxiv.org/abs/1705.04416

[3] A. Y. N. David M. Blei y M. I. Jordan, “Latent Dirichlet Allocation” https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf

[4] Q. Le y T. Mikolov, “Distributed Representations of Sentences and Documents” https://arxiv.org/pdf/1405.4053.pdf

[5] T. Hofmann, “Probabilistic Latent Semantic Analysis”, Proceedings of the Twenty-
Second Annual International SIGIR Conference on Research and Development in Information Retrieval (SIGIR-99) https://arxiv.org/abs/1301.6705
