# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 11:17:27 2014

@author: Daniel
"""

import gensim.models
from gensim.corpora import TextCorpus, MmCorpus, Dictionary
import nltk
from nltk.tokenize import RegexpTokenizer
import collections
from OdaGetter import *
import numpy as np

getter=OdaGetter()
LBcases=getter.get_LB_sager()

def feat_category(category_id):
    feat_array = np.zeros(17) # As oda.ft.dk distinguishes between 17 "case-categories" 
    feat_array[category_id-1] = 1
    return feat_array

ids=[]
for case in LBcases:
    ids.append(case['kategoriid'])
    
cats = list(set( ids ))
indexer = zip( range(len(cats)),cats)

np.zeros(len(cats))



X = np.array([[1,1,0,0],[1,-1,0,0],[1,0,0,0],[1,1,0,0]])

def remove_zero_cols(X):
    zero_cols = []
    for i in range( X.shape[1] ):
        if sum(X[:,i]) == 0:
            zero_cols.append(i)
        
    X=np.delete(X,zero_cols,1)
    return X
