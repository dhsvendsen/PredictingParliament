# -*- coding: utf-8 -*-

import numpy as np
import classifier_data


def test_feat_party():
    """Test if the relevant case can be found and the right feature array
    extracted
    """
    assert (classifier_data.feat_party(69) == np.array(
    [ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.])).all()
    
    
def test_feat_category():
    """Test if feature array generation is working
    """
    assert (classifier_data.feat_category(2) == np.array(
    [ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.,
     0.,  0.])).all()
     
def test_feat_L_or_B():
    """Test if feature array generation is working
    """
    assert (classifier_data.feat_L_or_B('L') == np.array([1., 0.])).all()