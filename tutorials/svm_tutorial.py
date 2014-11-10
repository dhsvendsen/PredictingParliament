# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 13:34:57 2014

@author: Daniel
"""

from sklearn import svm
X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC()
clf.fit(X, y) 