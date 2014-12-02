# -*- coding: utf-8 -*-

import sys; import os
sys.path.insert(0, os.path.abspath('..'))

import dataretrieval.odaparsers as opa
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle

all_mp = [(dicts['id'],dicts['navn']) for dicts in opa.all_MPs()]

DecisionTreeClassifier(max_depth=5)

predictions = []

A = np.zeros(52)

for mp in all_mp:
    try:
        with open('decisiontrees/classifier_{0}.pkl'.format(mp[0]), 'rb') as in_file:
            dtc = pickle.load(in_file)
        predictions.append((mp[1], dtc.predict(A)[0]))
    except IOError:
        print 'Actor of id {0} is not an actively voting MP'.format(mp[0])
        
from scipy import stats

final = stats.mode([tup[1] for tup in predictions])
