# -*- coding: utf-8 -*-

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import numpy as np
npt = np.testing
import classification.classifier_data as cda
import classification.resume_lda as res_lda


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
    """Test if function succesfully produces array."""
    assert cda.dataset_X_y(13).shape[0] > 10
    assert cda.dataset_X_y(13).shape[1] == 52
    assert type(cda.dataset_X_y) == np.ndarray
    
def test_resume_lda():
    pass
