# -*- coding: utf-8 -*-

"""Script containing testfunctions for the dataretrieval module"""

import os
PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)

import numpy as np
npt = np.testing
import dataretrieval.odagetter as oget
import dataretrieval.odaparsers as opa

# Tests for odagetter
GETTER = oget.OdaGetter()


def test_odata_with_db():
    GETTER.odata_with_db('http://oda.ft.dk/api/Afstemning?$inlinecount'
                         '=allpages', 'TEST')
    with open(PARENTDIR + '/storing/database/TEST.txt', 'r') as in_file:
        read = in_file.read()
        assert not read == None


def test_odata():
    """Test data retrieval with arbitrary url from oda.dt.dk"""
    req = GETTER.odata('http://oda.ft.dk/api/Afstemning?$inlinecount=allpages')
    assert req['value'][1]['vedtaget']


# Tests for odaparsers


def test_all_mps():
    """Test type and content dicts output"""
    all_mp = opa.all_mps()
    assert type(all_mp) == list
    assert 'Christine Antorini' in [dicts['navn'] for dicts in all_mp]
    assert len(all_mp) == 179


def test_single_mp():
    """Test successful retrieval of MP profile"""
    assert opa.single_mp(144)['navn'] == 'Helle Thorning-Schmidt'


def test_mp_votes():
    """Test successful retrieval of list of votes"""
    assert type(opa.mp_votes(138)[200]['typeid']) == int


def test_vote_case():
    """Test succesful retrieval of case-JSON based on case-id"""
    assert 'titel' in opa.vote_case(9)
