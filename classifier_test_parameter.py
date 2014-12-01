# -*- coding: utf-8 -*-
"""This script determines the most accurate classifier through parametrization
of classifiers. An MP id is chosen and a host of classifiers are trained on
the dataset and subsequently evaluated through stratisfied crossvalidation.
"""
from sklearn.cross_validation import StratifiedKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
import numpy as np
import classifier_data

mp_id = 5
try:
    X = np.load('data_matrices/X_{}.npy'.format(mp_id))
    y = np.load('data_matrices/y_{}.npy'.format(mp_id))
except IOError:
    X, y = classifier_data.dataset_X_y(mp_id)

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

def classifier_score(features, targets, classifier):
    """Performs stratisfied K-fold crossvalidation and for a classifier with a
    specified dataset. Then checks for the event that the trained classifier is
    trivial (all predictions equal to majority class).
    """
    K = 10
    cv = StratifiedKFold(targets, n_folds=K, indices=False)
    accuracies = []

    for train_index, test_index in cv:
        X_train, y_train = np.array(
            features[train_index]), np.array(targets[train_index])
        X_test, y_test = np.array(
            features[test_index]), np.array(targets[test_index])

        classifier.fit(X_train, y_train)
        accuracies.append(classifier.score(X_test, y_test))

    classifier.fit(features, targets)
    pred = classifier.predict(features)

    if np.mean(pred) % 1 == 0:
        print 'Classifier picks majority class as result for every prediction'
        return
    else:
        return np.mean(accuracies)

print 'Percentage of "yes"-votes cast in current period of government:',
np.mean(y == 1)
for name, clf in zip(names, classifiers):
    score = classifier_score(X, y, clf)
    print name, ' results are: \n', score
