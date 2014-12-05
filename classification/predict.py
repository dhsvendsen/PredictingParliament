# -*- coding: utf-8 -*-

import os
PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)

import dataretrieval.odaparsers as opa
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle

all_mp = [(dicts['id'],dicts['navn']) for dicts in opa.all_MPs()]
predictions = []
A = np.zeros(52)

for mp in all_mp:
    try:
        with open(PARENTDIR + '/storing/decisiontrees/classifier_%d.pkl' % mp,
                  'rb') as in_file:
            dtc = pickle.load(in_file)
        predictions.append((mp[1], dtc.predict(A)[0]))
    except IOError:
        print 'Actor of id {0} is not an actively voting MP'.format(mp[0])
        
from scipy import stats

final = stats.mode([tup[1] for tup in predictions])
