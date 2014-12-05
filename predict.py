# -*- coding: utf-8 -*-

"""This script allows the user to enter data and predict a vote.

In essence it works exactly the same as the webservice, just in a simple
command line version.
"""

import os
DIR = os.path.dirname(os.path.abspath(__file__))
os.sys.path.insert(0, DIR)

import dataretrieval.odaparsers as opa
import classification.resume_lda as res_lda
import numpy as np
import pickle
import pprint


def predict():
    """Start session and enter vote information to predict outcome."""
    pp = pprint.PrettyPrinter(indent=4)
    result = ['PASSED', 'DENIED']

    parties = [
        'Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
        'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
        'Liberal Alliance', 'Det Konservative Folkeparti']

    categories = [
        'Beretning af almen art', 'Alm. del', 'FT',
        'Henvendelser uden bilagsnummer', 'Mødesag', 'Info-noter',
        'US', 'Alm. del §-markeret', 'EU-noter',
        'B1 - Privat forslag - 1. (eneste) beh.', 'S',
        'Privat forslag',
        'Regeringsforslag', 'B3', 'B1 - Privat forslag',
        'B2', 'B1 - Regeringsforslag']

    all_mp = [(dicts['id'], dicts['navn']) for dicts in opa.all_mps()]
    predictions = []

    # feat_lda
    feat_lda = res_lda.lda_topics(raw_input('Enter resume: '))

    # feat_party
    party_map = zip(parties, range(len(parties)))
    feat_party = np.zeros(len(parties))

    print "Enter proposing party by integer from list:\n"
    pp.pprint(party_map)

    while True:
        inp = raw_input('\n')

        if inp.isdigit() and int(inp) in range(8):
            break
        else:
            print "Invalid entry"

    feat_party[int(inp)] = 1

    # feat_category
    category_map = zip(categories, range(len(categories)))
    feat_category = np.zeros(len(categories))

    print "\nEnter category by integer from list:\n"
    pp.pprint(category_map)

    while True:
        inp = raw_input('\n')

        if inp.isdigit() and int(inp) in range(17):
            break
        else:
            print "Invalid entry"

    feat_category[int(inp)] = 1

    # feat_LB
    print "\nEnter the type of proposition: bill (L) or motion (B):"
    while True:
        inp = raw_input('\n')

        if inp.lower() == 'l':
            feat_l_or_b = np.array([1, 0])
        elif inp.lower() == 'b':
            feat_l_or_b = np.array([0, 1])
        else:
            print "Invalid entry"
            continue
        print
        break

    data_object = np.hstack((feat_party, feat_category, feat_l_or_b, feat_lda))

    for mp in all_mp:
        try:
            with open(DIR + '/storing/classifiers/'
                      'classifier_{0}.pkl'.format(mp[0]), 'rb') as in_file:
                dtc = pickle.load(in_file)
            predictions.append((mp[1], dtc.predict(data_object)[0]))
        except IOError:
            print 'MP of ID {0} is not an actively voting MP\n'.format(mp[0])

    final = result[int(np.round(np.mean([tup[1] for tup in predictions])))-1]
    predictions = [i[1] for i in predictions]

    print "###############################"
    print "\tVote %s!" % final
    print "\tVotes for:\t", predictions.count(1)
    print "\tVotes against:\t", predictions.count(2)
    print "###############################"


if __name__ == '__main__':
    predict()
