# -*- coding: utf-8 -*-

import classifier_data
import odaparsers
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib
import pickle

all_mp = [dicts['id'] for dicts in odaparsers.all_MPs()]

DecisionTreeClassifier(max_depth=5)

#for mp_id in all_mp:
#	try:
#		X,y = classifier_data.dataset_X_y(mp_id)
#	except:
#		print "Failed to retrieve dataset for politician with ID:", mp_id
#		continue
#	np.save('X_{0}'.format(mp_id),X)
#	np.save('y_{0}'.format(mp_id),y)
	#dtc = DecisionTreeClassifier(max_depth=5).fit(X,y)
	#with open('classifier_{0}.pkl'.format(mp_id), 'wb') as out_file:
	#    pickle.dump(dtc, out_file) 
    

for mp_id in all_mp:
    X = np.load('data_matrices/X_{0}.npy'.format(mp_id))
    y = np.load('data_matrices/y_{0}.npy'.format(mp_id))
    if X.size == 0:
        print 'Actor of id {0} is not an actively voting MP'.format(mp_id)
    else:
        dtc = DecisionTreeClassifier(max_depth=5).fit(X,y)
        with open('decisiontrees/classifier_{0}.pkl'.format(mp_id), 'wb') as out_file:
            pickle.dump(dtc, out_file)
        print 'succesfully constructed decsion tree for mp of id{0}'.format(mp_id)
        
#X = np.load('classifiers/X_294.npy')
#y = np.load('classifiers/y_294.npy')        

#dtc = DecisionTreeClassifier(max_depth=5).fit(X,y)
#with open('classifier_294.pkl', 'wb') as out_file:
#    pickle.dump(dtc, out_file)

with open('decisiontrees/classifier_12.pkl', 'rb') as in_file:
    klas = pickle.load(in_file)
