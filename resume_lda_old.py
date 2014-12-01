# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 08:52:48 2014

@author: Daniel
"""
import gensim.models
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
import nltk
from nltk.tokenize import RegexpTokenizer
import collections
from OdaGetter import *
import numpy as np
import codecs

def lda_topics(resume):
    
    #n_topic = 6
    n_topic = 25
    tokenizer = RegexpTokenizer(r'[^\W\d_]\w+')
    
    try:
        #lda = gensim.models.LdaModel.load('lda_model_data/all_resume_model.model')
        lda = gensim.models.LdaModel.load('lda_model_data/all_resume_model_25.model')
        #dictionary = Dictionary.load('lda_model_data/all_resume_dict.dict')
        dictionary = Dictionary.load('lda_model_data/all_resume_dict_25.dict')
    except IOError:
        getter = OdaGetter()
        LBsager = getter.get_LB_sager()
        resume_body = []
        for case in LBsager:
            resume_body.append(case['resume'])
            
        with codecs.open('danish_stopwords.txt', 'r', encoding = 'UTF-8') as infile: # List of danish stopwords 
            stoplist = infile.read().split('\n')
   
        stoplist = [line.split() for line in stoplist]  
        stoplist = [line[0] for line in stoplist] + ['loven', 'lovens', 'iii', 
        'beslutningsforslag', 'lagde', 'angik', 'mens', 'idet', 'senere' ]

        # Identifying most used words for stopword list        
        allwords = []
        for doc in resume_body:
            allwords.extend(tokenizer.tokenize(doc))

        allwords = [word for word in allwords if word.lower() not in stoplist]
        fd = nltk.FreqDist(allwords)
        
        # Adding most frequently used words to stopwords list
        frequent_words = []
        for fd_tuple in collections.Counter(fd).most_common(200):
            frequent_words.append(fd_tuple[0].lower())
        stoplist = stoplist + frequent_words
        
        # Constructing text-corpus, a list of lists. The lists contain tokenized words of the resumes  
        texts = [[word.lower() for word in tokenizer.tokenize(document) if word.lower() not in stoplist] 
        for document in resume_body]
            
        # Dictionary to be used for Bag of Words (bow) representation of resumes
        dictionary = gensim.corpora.Dictionary(texts) 
        dictionary.save('lda_model_data/all_resume_dict.dict')
        
        # The corpus: a list of tuples (unique index from dictionary, numver of occurences)
        corpus = [dictionary.doc2bow(text) for text in texts]
        gensim.corpora.MmCorpus.serialize('lda_model_data/all_resume_corpus.mm', corpus)
        
        lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topic)
        lda.save('lda_model_data/all_resume_model.model')
        
    resume_bow = dictionary.doc2bow(tokenizer.tokenize( resume ))
    topic_array = np.zeros(n_topic)
    for topic in lda[resume_bow]:
        topic_array[ topic[0] ] = topic[1] * 5
        
    return topic_array
          
    