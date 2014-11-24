# -*- coding: utf-8 -*-
"""
Created on Mon Nov 24 13:46:38 2014

@author: Daniel
"""

import classifier_data
import OdaParser
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
import pickle

all_mp = [dicts['id'] for dicts in OdaParser.all_MPs()]

DecisionTreeClassifier(max_depth=5)

for mp_id in all_mp:
    X,y = classifier_data.dataset_X_y(mp_id)
    np.save('X_{0}'.format(mp_id),X)
    np.save('y_{0}'.format(mp_id),y)
    #dtc = DecisionTreeClassifier(max_depth=5).fit(X,y)
    #with open('classifier_{0}.pkl'.format(mp_id), 'wb') as out_file:
    #    pickle.dump(dtc, out_file) 
    

