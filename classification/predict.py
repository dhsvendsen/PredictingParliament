# -*- coding: utf-8 -*-

import os
PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)

import dataretrieval.odaparsers as opa
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle

all_mp = [(dicts['id'],dicts['navn']) for dicts in opa.all_mps()]
predictions = []



A = np.zeros(52)

for mp in all_mp:
    try:
        with open(PARENTDIR + '/storing/classifiers/'\
                  'classifier_{0}.pkl'.format(mp[0]), 'rb') as in_file:
            dtc = pickle.load(in_file)
        predictions.append((mp[1], dtc.predict(A)[0]))
    except IOError:
        print 'Actor of id {0} is not an actively voting MP'.format(mp[0])
        
final = np.round(np.mean([tup[1] for tup in predictions]))

print final
