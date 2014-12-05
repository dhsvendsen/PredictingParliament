# -*- coding: utf-8 -*-

"""This submodule handles parsing of data retrieved by 'odagetter' submodule.

Contains functions that parse methods from the 'odagetter.OdaGetter' class.
All of these functions, except for 'all_mps', are imported into the
'classification.classifier_data' submodule, to create arrays of features for
use in the 'dataset_X_y' function of this submodule. 'all_mps' is imported
into the main function 'generate_classifiers' and used for looping over all
MPs to train individual classifiers for each.
"""

import os
from dataretrieval.odagetter import OdaGetter
import re

PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)

GETTER = OdaGetter()


def all_mps():
    """Return clean list of MPs.

    This function creates a filtered version of
    'odagetter.OdaGetter.get_aktoer' that only contains acting and voting
    members of parliament (MPs) names and corresponding IDs. It is imported in
    the main function 'generate_classifiers'.

    Returns
    -------
    out : MP-list
        List-type record of all acting members of

        Example
        -------
        [
         {u'id': 5, u'navn': u'Frank Aaen'},
         {u'id': 12, u'navn': u'Nicolai Wammen'},
         {u'id': 13, u'navn': u'Sara Olsvig'},
         {u'id': 17, u'navn': u'Christine Antorini'},
         {u'id': 18, u'navn': u'Alex Ahrendtsen'},
         ...
        ]
    """
    with open(PARENTDIR + '/MF_list.txt', 'r') as in_file:
        mp_list_raw = in_file.read().decode('utf-8')
        pattern = re.compile(r'(.+)')
        mp_list = filter(lambda x: len(x) > 0,
                         [re.sub('\r', '', line)
                          for line in pattern.findall(mp_list_raw)])

    aktoer_raw = GETTER.get_aktoer()
    mps = filter(lambda x: x['navn'] in mp_list, aktoer_raw)[:179]

    mps_filtered = []

    for member in mps:
        mem_feats = {}
        for feature in member:
            if feature in ['navn', 'id']:
                mem_feat = {feature: member[feature]}
                mem_feats.update(mem_feat)
        mps_filtered.append(mem_feats)

    return mps_filtered


def single_mp(aktoerid):
    """Return profile for a given MP.

    This function uses 'odagetter.OdaGetter.get_aktoer' to pick out a single
    MP profile. It is imported in 'classification.classifier_data', and used
    in the function 'feat_party' of that submodule.

    Parameters
    ----------
    aktoerid : id-integer
        Int-type ID refering to a specific MP.

    Returns
    -------
    out : MP-dictionary
        Dict-type object that contains information about a single MP. Output
        is identical a list element of 'odagetter.OdaGetter.get_aktoer' return.
    """
    for mp in GETTER.get_aktoer():
        if aktoerid == mp['id']:
            return mp
    else:
        print "Found no MP for id %d" % aktoerid


def mp_votes(aktoerid):
    r"""Return clean list of votes cast by given MP.

    This function uses 'odagetter.OdaGetter.get_stemme' with an argument
    corresponding to the ID of an MP, and returns a clean list where all
    votes that are not of type 1 (FOR) or type 2 (AGAINST) are sorted out.
    It is imported in 'classification.classifier_data', and used in the
    function 'dataset_X_y' of that submodule, to through each vote the MP
    has cast and extract features from the corresponding cases.

    Parameter
    ---------
    aktoerid : id-integer
        Int-type ID refering to a specific MP.

    Returns
    -------
    out : data-list
        List-type JSON readable dataset.

        Example
        -------
        [
         {u'afstemningid': 1,
          u'akt\xf8rid': 5,
          u'id': 53,
          u'opdateringsdato': u'2014-09-09T09:05:59.653',
          u'typeid': 1},
          ...
        ]
    """
    stemmer = filter(lambda x: x['typeid'] in [1, 2],
                     GETTER.get_stemme(aktoerid))

    return stemmer


def vote_case(afstemningid):
    """Return case data for the prompted vote ID (da: 'afstemningid').

    This function uses 'odagetter.OdaGetter.get_afstemning' to pick out, for a
    given vote ID, the case stage ID (da: 'sagstrinid'), then uses
    'odagetter.OdaGetter.get_sagstrin' to get the case ID (da: 'sagid'), then
    uses 'odagetter.OdaGetter.get_sag' to get the case data for this case ID.
    It is imported in 'classification.classifier_data' and used in the function
    'dataset_X_y', where it offers a convenient way to access the needed data.

    Parameters
    ----------
    afstemningid : id-integer
        Int-type vote ID.

    Returns
    -------
    out : data-list
        Dictionary containing information about a given case. Return output is
        identical to that of 'odagetter.OdaGetter.get_sag'.
    """
    for afstemning in GETTER.get_afstemning():
        if afstemning['id'] == afstemningid:
            sagstrinid = afstemning['sagstrinid']
            break

    sagid = GETTER.get_sagstrin(sagstrinid)['sagid']

    return GETTER.get_sag(sagid)
