# Resource

* https://pathmind.com/wiki/
  * The Artificial Intelligence Wiki
* https://pathmind.com/wiki/python-ai
  * ogólna lista narzędzi, frameworków etc.

# Architektury

* LTSM
  * https://en.wikipedia.org/wiki/Long_short-term_memory
  * https://towardsdatascience.com/understanding-lstm-and-its-quick-implementation-in-keras-for-sentiment-analysis-af410fd85b47
* Markov Random Field
  * https://ermongroup.github.io/cs228-notes/representation/undirected/
  * https://en.wikipedia.org/wiki/Markov_random_field
* Hidden Markov Model
  * http://www.blackarbs.com/blog/introduction-hidden-markov-models-python-networkx-sklearn/2/9/2017
  * https://hmmlearn.readthedocs.io/en/latest/
  * https://en.wikipedia.org/wiki/Hidden_Markov_model

# Narzędzia

* https://github.com/TeamHG-Memex/eli5
  * "ELI5 is a Python package which helps to debug machine learning classifiers and explain their predictions."
  * Do wskazywania interesujących fragmentów DNA


# Podobne projekty

* VIDHOP (VIrus Deep learning HOst Prediction)
  * https://www.biorxiv.org/content/10.1101/575571v1
  * Metody:
    * **LSTM**
      * "The architecture of our first model consists of a three bidirectional LSTM layers"
      * "This bidirectional LSTM tries to find longterm context in the input sequence data, presented to the model in forward and reverse direction"
    * **CNN + LSTM**
      * "two layers of convolutional neural networks (CNN) nodes, followed by two bidirectional LSTM layers and two dense layers"
      * "The idea behind this architecture is that the CNN identifies important sequence parts (first layer), combines the short sequence features to more complex patterns (second layer), which can then be put into context by the LSTMs, which are able to remember previously seen patterns."
  * Wyniki:
    * Testowali dla różnych datasetów (rotawirus, wścieklizna, grypa) dla różnych gatunków (człowiek, ptaki etc.), spore różnice w accuracy między nimi
    * CNN + LSTM gorsze średnio o ~4% przy celności
    * "The **best performing architecture was the LSTM**, achieving the highest accuracy for all three datasets. Nevertheless, for a fast prototyping it makes sense to use **CNN+LSTM as it trains around 4 times faster and reaches comparable results**. Furthermore the **CNN+LSTM architecture showed no difficulty in learning long input sequences**, while the LSTM architecture frequently remained in a state of random accuracy for a long time during training."
  * Dodatkowe info:
    * Deep learning outperforms other approaches

---

* HostPhinder: A Phage Host Prediction Tool
  * https://backend.orbit.dtu.dk/ws/portalfiles/portal/125058499/HostPhinder.pdf
  * Metody:
    * "HostPhinder predicts the host species of a query phage as the host of the most genomically similar reference phages. As a measure of genomic similarity the number of co-occurring k-mers is used."
    * Oparty na analizie skupień i dystansach 16-merów
  * Wyniki:
    * Accuracy 78%-79% dla gatunku, 82%-83% dla rodzaju
    * Niewiele lepszy od BLASTa

---

*  VirHostMatcher-Net: A network-based integrated framework for predicting virus-host interactions
   * https://www.biorxiv.org/content/10.1101/505768v2.full
   * Metody:
     * Markov Random Field (???) przy użyciu CRISPR sequences, sequence homology, and alignment-free similarity measures
     * Łączy hosty z hostami, virusy z virusami i hosty z virusami, doczytaj
   * Wyniki:
     * Accuracy 62% dla rodzaju, 85% dla gromady 

---

* Predicting virus-host association by Kernelized logistic matrix factorization and similarity network fusion
  * https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-3082-0
  * Metody:
    * Graf możliwych połączeń par pozytywnych i negatywnych
    * Finally, similarities between viruses are calculated by oligonucleotide frequency (ONF) measures and expressed by Sv∈RNv×NvSv∈RNv×Nv; similarities between hosts are calculated by integrating ONF measures and Gaussian interaction profile (GIP) kernel similarity based on SNF model, and expressed by Sh∈RNh×NhSh∈RNh×Nh. (???)
    * https://github.com/liudan111/ILMF-VH
  * Wyniki:
    * 58.9%, podbite do 63,6% dodając konsensus top 5 wyników
  * Dodatkowe info:
    * https://towardsdatascience.com/probabilistic-matrix-factorization-b7852244a321 

# Luźne info

* https://github.com/jessieren/VirHostMatcher
  * "This program is used to compute various oligonucleotide frequency (ONF) based distance/dissimialrity measures between a pair of DNA sequences. Computing these measures with VirHostMatcher is specifically used to predict the potential host of a query virus by identifying the host to which it has the strongest similarity."

# Pomysły

* Przewidywanie sekwencji hosta + blast
* virus-host shared CRISPR