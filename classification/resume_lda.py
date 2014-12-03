# -*- coding: utf-8 -*-

from dataretrieval.odagetter import OdaGetter
from gensim import corpora, models
from gensim.utils import simple_preprocess
import nltk
import nltk.corpus
import numpy as np
import os

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)


def lda_topics(resume):
    """Perform Latent Dirichlet Analysis on a string. The corpus of all case
    resumes (in BOW representation) is transformed by 'term frequency–inverse
    document frequency' method.

    Parameters
    ----------
    resume : string
        An arbitrary string on which LDA analysis will be performed

    Returns
    -------
    out : topic-array
        A numpy array of n_topic length with topic weighs
    """

    n_topic = 25

    # Attempt to retrieve stored LDA model
    try:
        lda = models.LdaModel.load(
            'storing/ldamodel/all_resume_model_modified_%s.model' % str(
                n_topic))
        dictionary = corpora.Dictionary.load(
            'storing/ldamodel/all_resume_dict_modified_%s.dict' % str(
                n_topic))

    except IOError:
        # Retrieve all resumes
        getter = OdaGetter()
        cases = getter.get_LB_sager()

        # Create text corpus, using utf-8 encoding
        corpus = [case['resume'].encode('utf-8') for case in cases
                  if len(case['resume']) > 1]

        stoplist = [stopword.encode('utf-8') for stopword
                    in nltk.corpus.stopwords.words('danish')]

        corpus = [[word for word in document.lower().split()
                  if word not in stoplist] for document in corpus]  # Tokenize

        all_tokens = sum(corpus, [])
        tokens_once = set(word for word in set(all_tokens)
                          if all_tokens.count(word) == 1)
        corpus = [[word for word in text if word not in tokens_once]
                  for text in corpus]

        # Create dictionary that maps words to word ids
        dictionary = corpora.Dictionary(corpus)
        dictionary.save(
            'storing/ldamodel/all_resume_dict_modified_%s.dict' % str(n_topic))

        # Bag of words (BOW) representation of corpus
        corpus_bow = [dictionary.doc2bow(document) for document in corpus]
        corpora.MmCorpus.serialize(
            'storing/ldamodel/all_resume_corpus_modified_%s.mm' % str(n_topic),
            corpus_bow)

        # Transform BOW corpus using 'term frequency–inverse document
        # frequency'. This is necessary to weight the importance of words.
        tfidf = models.TfidfModel(corpus_bow)
        corpus_tfidf = tfidf[corpus_bow]

        # Train and save LDA model
        lda = models.ldamodel.LdaModel(
            corpus=corpus_tfidf, id2word=dictionary, num_topics=n_topic)
        lda.save(
            'storing/ldamodel/all_resume_model_modified_%s.model' % str(
                n_topic))

    resume_bow = dictionary.doc2bow(simple_preprocess(resume))
    resume_lda = lda[resume_bow]

    topic_array = np.zeros(n_topic)
    for topic in resume_lda:
        topic_array[topic[0]] = topic[1]

    return topic_array
