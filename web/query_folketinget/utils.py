# -*- coding: utf-8 -*-

from os.path import abspath, dirname, realpath, join
import os
import sys

PPARENTDIR = dirname(dirname(dirname(abspath(__file__))))
os.sys.path.insert(0, PPARENTDIR)

import dataretrieval.odaparsers as opa
import pickle

def predict_votes(data_object):
    """Predict votes of members of parliament (MPs) using classifiers.
    """
    predictions = []
    all_mp = [(dicts['id'], dicts['navn']) for dicts in opa.all_mps()]
    for mp in all_mp:
        classifier_path = join(
            dirname(realpath(__file__)),
            PPARENTDIR + '/storing/classifiers/classifier_{0}.pkl'.format(mp[0])
        )
        try:
            with open(classifier_path, 'rb') as in_file:
                #print in_file
                dtc = pickle.load(in_file)
            predictions.append((mp[1], dtc.predict(data_object)[0]))
        except IOError:
            print 'Actor of id {0} is not an actively voting MP'.format(mp[0])
    return predictions