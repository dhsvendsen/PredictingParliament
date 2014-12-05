# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities
from gensim.utils import simple_preprocess
import nltk
import nltk.corpus
from nltk.tokenize import RegexpTokenizer
import collections
from odagetter import OdaGetter
import numpy as np
import codecs
import sys
import os


def lda_topics(resume):
    
    n_topic = 25
    tokenizer = RegexpTokenizer(r'[^\W\d_]\w+')

    one = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lda_model_data/all_resume_model_modified_25.model')
    two = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lda_model_data/all_resume_dict_modified_25.dict')
    three = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lda_model_data/all_resume_corpus_modified_25.mm')


    try:
        lda = models.LdaModel.load(one)
        dictionary = corpora.Dictionary.load(two)

    except IOError:
        # Retrieve all resumes
        getter = OdaGetter()
        cases = getter.get_LB_sager()


        # Create text corpus.
        corpus = [case['resume'].encode('utf-8') for case in cases
            if len(case['resume']) > 1] # unicode -> utf-8

        stoplist = [stopword.encode('utf-8') for stopword 
            in nltk.corpus.stopwords.words('danish')] # unicode -> utf-8

        corpus = [[word for word in document.lower().split() 
                    if word not in stoplist] 
                    for document in corpus] # Tokenizing

        all_tokens = sum(corpus, [])
        tokens_once = set(word for word in set(all_tokens) 
            if all_tokens.count(word) == 1)
        corpus = [[word for word in text if word not in tokens_once]
            for text in corpus]


        # Create dictionary that maps words to word ids
        dictionary = corpora.Dictionary(corpus) 
        dictionary.save(two)


        # Bag of words (BOW) representation of corpus
        corpus_bow = [ dictionary.doc2bow(document) for document in corpus]
        corpora.MmCorpus.serialize(three, corpus_bow)


        # Transform BOW corpus using 'term frequency–inverse document 
        # frequency'. This is necessary to weight the importance of words.
        tfidf = models.TfidfModel(corpus_bow)
        corpus_tfidf = tfidf[corpus_bow]


        # Train and save LDA model
        lda = models.ldamodel.LdaModel(
            corpus=corpus_tfidf, id2word=dictionary, num_topics=n_topic)
        lda.save(one)

        #print lda.print_topics(n_topic)


    resume_bow = dictionary.doc2bow(simple_preprocess(resume))
    resume_lda = lda[resume_bow]

    topic_array = np.zeros(n_topic)
    for topic in resume_lda:
        topic_array[ topic[0] ] = topic[1]

    return topic_array
