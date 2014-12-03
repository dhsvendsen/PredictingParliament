# -*- coding: utf-8 -*-

import sys; import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import numpy as np
import classification.classifier_data as cda


def test_feat_party():
    """Test if the relevant case can be found and the right feature array
    extracted
    """
    assert (cda.feat_party(69) == np.array(
    [ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.])).all()
    
    
def test_feat_category():
    """Test if feature array generation is working
    """
    assert (cda.feat_category(2) == np.array(
    [ 0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., 0.,  0.,
     0.,  0.])).all()
     
def test_feat_L_or_B():
    """Test if feature array generation is working
    """
    assert (cda.feat_L_or_B('L') == np.array([1., 0.])).all()
    
    #blabalba
