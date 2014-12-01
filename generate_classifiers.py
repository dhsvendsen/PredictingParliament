# -*- coding: utf-8 -*-
"""This script calls the dataset_X_y from classifier_data.py to generate a data
matrix and class index for each member of parliament and subsequently trains a
decision tree classifier - the classifier found to be most effective. Data
matrices and classifiers are saved to .npy and .pkl files respectively.
"""
import classifier_data
import odaparsers
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle

all_mp = [dicts['id'] for dicts in odaparsers.all_MPs()]

DecisionTreeClassifier(max_depth=5)

for mp_id in all_mp:
    X, y = classifier_data.dataset_X_y(mp_id)
    np.save('data_matrices/X_{0}'.format(mp_id), X)
    np.save('data_matrices/y_{0}'.format(mp_id), y)
    if X.size == 0:
        print 'Actor of id {0} is not an active member of the parliament'.format(mp_id)
    else:
        dtc = DecisionTreeClassifier(max_depth=5).fit(X, y)
        with open('decisiontrees/classifier_{0}.pkl'.format(
                mp_id), 'wb') as out_file:
            pickle.dump(dtc, out_file)
