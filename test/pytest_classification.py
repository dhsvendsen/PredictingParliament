# -*- coding: utf-8 -*-

"""Script containing testfunctions for the classification module"""

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import numpy as np
npt = np.testing
import classification.classifier_data as cda
import classification.resume_lda as res_lda
import classification.classifier_test_parameter as ctp

# Tests for classifier_data (cda)


def test_feat_party():
    """Test if relevant case can be found and right feature-array extracted."""
    npt.assert_array_equal(cda.feat_party(69),
                           [0., 0., 0., 0., 1., 0., 0., 0.])


def test_feat_category():
    """Test if feature array generation is working."""
    npt.assert_array_equal(cda.feat_category(2),
                           [0., 1., 0., 0., 0., 0., 0., 0.,
                            0., 0., 0., 0., 0., 0., 0., 0., 0.])


def test_feat_L_or_B():
    """Test if feature array generation is working."""
    npt.assert_array_equal(cda.feat_L_or_B('L'), [1., 0.])


def test_remove_zero_cols():
    """Test if function succesfully removes zero-coloumns."""
    A = np.array([[1, 0, 4], [2, 0, 5]])
    B = np.array([[1, 4], [2, 5]])
    npt.assert_array_equal(cda.remove_zero_cols(A), B)


def test_dataset_X_y():
    """Test if function succesfully produces arrays."""
    X, y = cda.dataset_X_y(17)
    print X.shape
    assert X.shape[0] > 10
    assert X.shape[1] == 52
    assert len(X) == len(y)
    assert type(X) == np.ndarray
    assert type(y) == np.ndarray

# Tests for resume_lda (res_lda)


def test_lda_topics():
    """Test that the right dimension of np.array of correct order of mag."""
    topics = res_lda.lda_topics('Loven om at alle skal spise sushi mindst en '
                                'gang om ugen')
    assert type(topics) == np.ndarray
    npt.assert_array_almost_equal(topics, np.ones(25) * 0.5, decimal=0)

# Tests for classifier_test_parameter (ctp)


def test_classifier_score():
    """Test for successful output in the interval [0; 1]."""
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier(max_depth=5)
    X, y = cda.dataset_X_y(23)
    acc = ctp.classifier_score(X, y, clf)
    assert acc >= 0 and acc <= 1
