# -*- coding: utf-8 -*-
"""This module contains functions, each returning a zero-array which holds a
single 1 representing the precense of a feature in a case (data object). These
arrays are combined into a data object row and then a full data matrix by the
dataset_X_y(aktoerid) function of this module.
Note that in some cases a feature may not be present for an
observation, in which case the function will just return the zero-array. Full
rows of zeros, i.e. features that were never present will be deleted in the
final step of this script.
"""

import sys; import os
sys.path.insert(0, os.path.abspath('..'))

from dataretrieval.odagetter import OdaGetter
from dataretrieval.odaparsers import single_MP, MP_votes, vote_case
from resume_lda import lda_topics
import xml.etree.ElementTree as ET
import numpy as np

getter = OdaGetter()


def feat_party(caseid):
    """Return feature array representing the party of the proposing MP (PMP).
    """

    parties = ['Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
                'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
                'Liberal Alliance', 'Det Konservative Folkeparti']

    try:
        aktoerid = getter.get_sagaktoer(caseid, 19)  # 19 is the typeid for
        # the "proposing politician
    except IndexError:
        print "No actor with role id 19 was found for\ caseid %d. Returning \
        0-array." % caseid
        return np.zeros(len(parties))

    data = single_MP(aktoerid)

    try:
        root = ET.fromstring(data['biografi'].encode('utf-16'))
    except:
        print "No info ('biografi') was found for MP: %s. Returning\
        0-array." % aktoerid
        return np.zeros(len(parties))

    party = root.find('party').text

    feat_array = np.zeros(len(parties))

    for i, p in enumerate(parties):
        if party == p:
            feat_array[i] = 1
            break
    else:
        print "No party was found for caseid: %d. Returning 0-array." % caseid

    return feat_array


def feat_category(case_categoryid):
    """Return feature array representing the category of the proposition.
    """
    feat_array = np.zeros(17)  # There are 17 different categories
    feat_array[case_categoryid-1] = 1

    return feat_array


def feat_L_or_B(case_nummerprefix):
    """Return feature array representing whether proposition is bill (L) or
    motion (B).
    """
    if case_nummerprefix == 'L':
        return np.array([1., 0.])
    elif case_nummerprefix == 'B':
        return np.array([0., 1.])
    else:
        return np.array([0., 0.])


def remove_zero_cols(X):
    """Takes a numpy array or matrix and removes coloumns that consist only of
    zeros
    """
    zero_cols = []
    for i in range(X.shape[1]):
        if sum(X[:, i]) == 0:
            zero_cols.append(i)

    X = np.delete(X, zero_cols, 1)
    return X


def dataset_X_y(aktoerid):
    """Return a clean dataset X of features for every case the given MP has
    voted in, along with a target vector y, representing his/her vote in said
    case.
    """

    # Get list of votes that the given MP has cast
    MP_votes_list = MP_votes(aktoerid)

    # Get full list of votes in parliament. This is needed since we are only
    # interested in votes that are of typeid = 1, i.e. final votes, and this
    # information is not available in MP_votes_list. Note that the key 'typeid'
    # is also present in MP_votes_list, but that it here represents the MP's
    # decision in that vote, and carries no information about what type of
    # vote it was.
    all_votes_list = getter.get_afstemning()

    # The database has a lot of dublicates, so to avoid these we add processed
    # cases to an array that has to be checked for every iteration.
    processed_cases = []

    X, y = [], []
    for MP_vote in MP_votes_list:

        # Check if vote is final, i.e. typeid = 1
        continue_after_check = True
        for vote in all_votes_list:
            if MP_vote['afstemningid'] == vote['id']:
                if vote['typeid'] != 1:
                    continue_after_check = False
                    print "Vote not final"
                    break

        if continue_after_check is False:
            continue

        # Instantiate case profile to extract features from
        case = vote_case(MP_vote['afstemningid'])

        if case['id'] in processed_cases:
            print "Dublicate found! Vote %d in case %d" % (
            MP_vote['afstemningid'], case['id'])
            continue
        else:
            processed_cases.append(case['id'])

        print "\nProcessing vote %d in case %d - MP id %d\n" % (
        MP_vote['afstemningid'], case['id'], aktoerid)

        X_case = []

        X_case.extend(feat_party(case['id']))
        print "Successfully added party\t to features for\
        caseid\t %d" % case['id']

        X_case.extend(feat_category(case['kategoriid']))
        print "Successfully added category\t to features for\
        caseid\t %d" % case['id']

        X_case.extend(feat_L_or_B(case['nummerprefix']))
        print "Successfully added numberprefix\t to features for\
        caseid\t %d" % case['id']

        X_case.extend(lda_topics(case['resume']))
        print "Successfully added LDA topics\t to features for\
        caseid\t %d" % case['id']

        X.append(X_case)
        y.append(MP_vote['typeid'])

    return np.array(X), np.array(y)
