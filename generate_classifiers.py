# -*- coding: utf-8 -*-
"""This script functions as the main function of the entire program.

It calls the dataset_X_y from classification.classifier_data to generate a data
matrix and class index for each member of parliament and subsequently trains a
decision tree classifier - the classifier found to be most effective. Data
matrices and classifiers are saved to .npy and .pkl files respectively.
"""

import classification.classifier_data as cd
import dataretrieval.odaparsers as opa
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle

all_mp = [dicts['id'] for dicts in opa.all_MPs()]

for mp_id in all_mp:
    X, y = cd.dataset_X_y(mp_id)
    np.save('storing/matrices/X_{0}'.format(mp_id), X)
    np.save('storing/matrices/y_{0}'.format(mp_id), y)
    if X.size == 0:
        print 'Actor of id {0} is not an active member of the parliament'.format(mp_id)
    else:
        dtc = DecisionTreeClassifier(max_depth=5).fit(X, y)
        with open('storing/classifiers/classifier_{0}.pkl'.format(
                mp_id), 'wb') as out_file:
            pickle.dump(dtc, out_file)
