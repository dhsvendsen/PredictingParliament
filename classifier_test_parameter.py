# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 15:58:00 2014

@author: Daniel
"""

from resume_lda import *
from classifier_data import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
import numpy as np

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes", "LDA", "QDA"]
classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=200),
    AdaBoostClassifier(),
    GaussianNB(),
    LDA(),
    QDA()]

#X = np.load('lda_model_data/X_25.npy')
#X = np.load('lda_model_data/X_25_w0.npy')
#y = np.load('lda_model_data/y_25.npy')
#y = np.load('lda_model_data/y_25_w0.npy')

#X = np.load('X_frank.npy')
#y = np.load('y_frank.npy')

#X,y = dataset_X_y(5)
#np.save('lda_model_data/X_5_no_ministry_no_category',X)
#np.save('lda_model_data/y_5_no_ministry_no_category,y)

X = np.load('lda_model_data/X_5_no_ministry.npy')
y = np.load('lda_model_data/y_5_no_ministry.npy')

print 'optimism level of politician is', 1-np.mean(y-1)

def classifier_score(features, targets, classifier):
    K = 10
    cv = cross_validation.StratifiedKFold(targets, n_folds=K, indices=False)
    accuracies = []

    for train_index, test_index in cv:
        X_train, y_train  = np.array(features[train_index]) ,np.array(targets[train_index])
        X_test, y_test  = np.array(features[test_index]) ,np.array(targets[test_index])

        classifier.fit(X_train, y_train)
        accuracies.append(classifier.score(X_test, y_test))
        
    classifier.fit(features, targets)
    pred = classifier.predict(features)
    
    if np.mean(pred)%1 == 0:
        print 'Classifier picks majority class as result every time'
        return
    else:
        return np.mean(accuracies)
        
for name, clf in zip(names, classifiers):
    score = classifier_score(X, y, clf)
    print name, ' results are: \n', score
    

        
#####################SAVE KLASI#######################
#import pickle        
#dtc = DecisionTreeClassifier(max_depth=5).fit(X,y)
#with open('tree_dump_test.pkl', 'wb') as out_file:
#    pickle.dump(dtc, out_file)    
#
#with open('tree_dump_test.pkl', 'rb') as in_file:
#    loadedbusiness = pickle.load(in_file)