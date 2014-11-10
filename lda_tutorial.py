# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 15:16:33 2014

@author: Daniel
"""
import logging, sys, pprint
import gensim
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
import nltk
from nltk.tokenize import RegexpTokenizer
import collections

import OdaParser
from OdaGetter import *

getter = OdaGetter()

#def get_MP_resumes(aktoerid):
#    """
#        Returns a list of tuples, each representing a datapoint for the classifier.
#        Example [({FEATURES}, yes), 
#                 ({FEATURES}, no), 
#                 ({FEATURES}, no), ...]
#    """
#    resume = []
#    votings=getter.get_afstemning()
#    for i, vote in enumerate(OdaParser.get_MP_votes(aktoerid)):
#        if not votings[i]['typeid'] == 1:
#            continue
#        case = OdaParser.get_case(vote['afstemningid'])
#        resume.append(case['resume']+case['titelkort'])
#    
#    return list(set(resume))
#
## Which actor id to perform LDA for
#actor_id = 5
#resume_body = get_MP_resumes(actor_id)

LBsager = getter.get_LB_sager()
resume_body = []
for case in LBsager:
    resume_body.append(case['resume'])
#%%
# List of danish stopwords from http://snowball.tartarus.org/algorithms/danish/stop.txt
with open('danish_stopwords.txt','r') as infile: 
    stoplist = infile.read().split('\n')
   
stoplist = [line.split() for line in stoplist]  
stoplist = [line[0] for line in stoplist] + ['loven',
'lovens', 'beslutningsforslag' ] # Appending words without information

# Identifying most used words for stopword list
tokenizer = RegexpTokenizer(r'[^\W\d_]\w+')
allwords = []
for doc in resume_body:
    allwords.extend(tokenizer.tokenize(doc))

allwords = [word for word in allwords if word.lower() not in stoplist]
fd = nltk.FreqDist(allwords)
#fd.plot(100,cumulative=False) 

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
dictionary.save('lda_dicts_corpora/corpora_actor5.dict')

#print dictionary # returns number of unique tokens found
#print(dictionary.token2id) # returns the dictionary containing {keys=unique words : value=unique index}

# The corpus: a list of tuples (unique index from dictionary, numver of occurences)
corpus = [dictionary.doc2bow(text) for text in texts]
gensim.corpora.MmCorpus.serialize('lda_dicts_corpora/corpora_actor5.mm', corpus)

n_topic = 6
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=n_topic)

# Printing topics
for i in range(0, lda.num_topics-1):
    print lda.print_topic(i)

# Now we can assert a topic distribution
example_text = resume_body[22]
example_bow = dictionary.doc2bow(tokenizer.tokenize( example_text ))
print lda[example_bow]

# reduced number of topics from 10 because more interpretable topics were generated
# and the analysis showed all topics getting > 96% accuracy only one topic.
# With fewer topics the resumes become a mixture of topics


