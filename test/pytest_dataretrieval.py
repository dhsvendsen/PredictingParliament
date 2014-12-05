# -*- coding: utf-8 -*-

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import numpy as np
from dataretrieval import odagetter, odaparsers


def test_feat_party():
    """Test if the relevant case can be found and the right feature array
    extracted
    """
    assert (cda.feat_party(69) == np.array(
    [ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.])).all()
