# -*- coding: utf-8 -*-

import os
PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)

import dataretrieval.odaparsers as opa
import classification.resume_lda as res_lda
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle

all_mp = [(dicts['id'], dicts['navn']) for dicts in opa.all_mps()]
predictions = []


# feat_lda
feat_lda = res_lda.lda_topics(raw_input('Enter resume: '))


# feat_party
parties = ['Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
           'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
           'Liberal Alliance', 'Det Konservative Folkeparti']
party_map = dict(zip(parties, range(len(parties))))
feat_party = np.zeros(len(parties))
feat_party[party_map[raw_input('Enter proposing party from list:'
                               '\n \n %s \n \n' % ', '.join(parties))]] = 1


# feat_cat
categories = ['Beretning af almen art', 'Alm. del', 'FT',
              'Henvendelser uden bilagsnummer', 'Mødesag', 'Info-noter', 'US',
              'Alm. del §-markeret', 'EU-noter',
              'B1 - Privat forslag - 1. (eneste) beh.', 'S', 'Privat forslag',
              'Regeringsforslag', 'B3', 'B1 - Privat forslag',
              'B2', 'B1 - Regeringsforslag']
category_map = dict(zip(categories, range(len(categories))))
feat_category = np.zeros(len(categories))
feat_category[category_map[raw_input('Enter proposing party from list:\n \n %s'
                                     '\n \n' % ', '.join(categories))]] = 1


# feat_LB
if raw_input('Enter the type of proposition: bill (L) or motion (B): ') == 'L':
    feat_L_or_B = np.array([1, 0])
else:
    feat_L_or_B = np.array([0, 1])

data_object = np.hstack(feat_party, feat_category, feat_L_or_B, feat_lda)

for mp in all_mp:
    try:
        with open(PARENTDIR + '/storing/classifiers/'
                  'classifier_{0}.pkl'.format(mp[0]), 'rb') as in_file:
            dtc = pickle.load(in_file)
        predictions.append((mp[1], dtc.predict(data_object)[0]))
    except IOError:
        print 'Actor of id {0} is not an actively voting MP'.format(mp[0])

final = int(np.round(np.mean([tup[1] for tup in predictions])))

print final
