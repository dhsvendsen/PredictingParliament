# -*- coding: utf-8 -*-

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

import numpy as np
npt = np.testing
import dataretrieval.odagetter as oget
import dataretrieval.odaparsers as opa

# Tests for odagetter
#GETTER = oget.OdaGetter(?!?!?!)


def test_hmmm():
    pass
    
    
# Tests for odagetter


def test_all_mps():
    all_mp = opa.all_mps()
    assert type(all_mp) == list
    assert 'Christine Antorini' in [dicts['navn'] for dicts in all_mp]
    #assert all_mp[3]['navn'] == 'Christine Antorini'
    assert len(all_mp) == 179

