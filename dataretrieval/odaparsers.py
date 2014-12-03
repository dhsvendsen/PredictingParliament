# -*- coding: utf-8 -*-

"""This module deals with the parsing of data from ODA into a format that
is understood by a classifier. 'dataset_X_y()' is called for
each MP to return a list of tuples that can be used to train a classifier.
'all_MPs' is called as an array to loop over to generate train data for
each MP decision classifier.
"""

from odagetter import OdaGetter
import re
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

getter = OdaGetter()


def all_MPs():
    """Return a filtered version of get_aktoer() that only contains MPs and
    id and name for each.
    """

    # Create a clean list of MPs from file.
    with open('MF_list.txt', 'r') as in_file:
        MP_list_raw = in_file.read().decode('utf-8')
        pattern = re.compile(r'(.+)')
        MP_list = filter(lambda x: len(x) > 0,
                         [re.sub('\r', '', line)
                          for line in pattern.findall(MP_list_raw)])

    aktoer_raw = getter.get_aktoer()
    MPs = filter(lambda x: x['navn'] in MP_list, aktoer_raw)[:179]

    MPs_filtered = []

    for member in MPs:
        mem_feats = {}
        for feature in member:
            if feature in ['navn', 'id']:
                mem_feat = {feature: member[feature]}
                mem_feats.update(mem_feat)
        MPs_filtered.append(mem_feats)

    return MPs_filtered


def single_MP(aktoerid):
    """Return profile for the prompted MP.
    """

    for MP in getter.get_aktoer():
        if aktoerid == MP['id']:
            return MP
    else:
        print "Found no MP for id %d" % aktoerid


def single_PMP(aktoerid):
    """Return profile for the prompted PMP.
    """

    for PMP in getter.get_ministeromraaede_aktoer():
        if aktoerid == PMP['id']:
            return PMP
    else:
        print "Found no PMP for id %d" % aktoerid


def MP_votes(aktoerid):
    """Return a JSON containing vote type and references to each vote a
    member has cast.
    """

    stemmer = filter(lambda x: x['typeid'] in [1, 2],
                     getter.get_stemme(aktoerid))

    return stemmer


def vote_case(afstemningid):
    """Return case profile for the prompted vote id.
    """

    for afstemning in getter.get_afstemning():
        if afstemning['id'] == afstemningid:
            sagstrinid = afstemning['sagstrinid']
            break

    sagid = getter.get_sagstrin(sagstrinid)['sagid']

    return getter.get_sag(sagid)
