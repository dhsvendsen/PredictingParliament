from resume_lda import *
from classifier_data import *
from classifier_test import *

X, y = dataset_X_y(5)

print

print "Classifier accuracy: %d" % sklearn_classifier_Kfold_score(X,y)