# This module deals with the parsing of data from ODA into a format that
# is understood by a classifier. 'get_MP_classifier_array' is called for
# each MP to return a list of tuples that can be used to train a classifier.
# 'get_MPs' is called as an array to loop over to generate train data for
# each MP decision classifier.

from OdaGetter import *

import json
import re
from pprint import pprint as pp
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn import cross_validation
import numpy as npsudo 



getter = OdaGetter()



def get_MPs():
    """
        Returns a filtered version of get_aktoer() that only contains MPs and
        id and name for each.
    """

    # Create a clean list of MPs from file.

    with open('junk/MF_list.txt','r') as in_file:
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
                mem_feat = {feature : member[feature]}
                mem_feats.update(mem_feat)
        MPs_filtered.append(mem_feats)
            

    return MPs_filtered



### Write function that analyses resumes and titles for topics, using gensim LDA.

### Write function that returns the most probable topic for a title.

### Write function that returns the most probable topic for a resume.

### Write function that can be used to implement bill/motion author in feature set.



def get_MP_votes(aktoerid):
    """
        Returns a JSON containing vote type and references to each vote a 
        member has cast.
    """

    for aktoer in get_MPs():
        if aktoer['id'] == aktoerid:
            stemmer = filter(lambda x: x['typeid'] in [1, 2], 
                             getter.get_stemme(aktoer['id']))

            return stemmer



def get_case(afstemningid):
    """
        Returns a case JSON from a vote id.
    """

    for afstemning in getter.get_afstemning():
        if afstemning['id'] == afstemningid:
            sagstrinid = afstemning['sagstrinid']
            break


    sagid = getter.get_sagstrin(sagstrinid)['sagid']


    return getter.get_sag(sagid)



def get_case_MP(caseid):
    pass



def get_case_ministry(caseid):
    pass



def get_MP_classifier_data_nltk(aktoerid):
    """
        Returns a list of tuples, each representing a datapoint for the classifier.
        Example [({FEATURES}, yes), 
                 ({FEATURES}, no), 
                 ({FEATURES}, no), ...]
    """

    votings         = getter.get_afstemning()
    X = []
    y = []


    for i, vote in enumerate(get_MP_votes(aktoerid)):
        if votings[i]['typeid'] != 1:
            continue
        case = get_case(vote['afstemningid'])
        features = {#'title' : case['titel'],
                    'len of title' : len(case['titel']),
                    'type of proposition' : case['nummerprefix'],
                    'category id' : case['kategoriid'],
                    #'resume': case['resume'],
                    'len of resume' : len(case['resume']),
                    'title card' : case['titelkort'],
                    'type id' : case['typeid']}
        
        X.append(features)
        y.append(vote['typeid'])
    

    return zip(feature_array,decision_array)



def get_MP_classifier_data_sklearn(aktoerid):
    """
        Returns two lists feature_array and decision_array.
    """

    votings         = getter.get_afstemning()
    feature_array   = []
    target_array    = []


    for i, vote in enumerate(get_MP_votes(aktoerid)):
        
        if votings[i]['typeid'] != 1:
            continue

        case = get_case(vote['afstemningid'])

        if case['nummerprefix'] == 'L':
            numberprefixid = 1
        elif case['nummerprefix'] == 'B':
            numberprefixid = 2
        elif not case['nummerprefix'] in ['A','B']:
            continue

        features = [#case['titel'],
                    len(case['titel']),
                    numberprefixid,
                    case['kategoriid'],
                    #case['resume'],
                    len(case['resume']),
                    #case['titelkort'],
                    case['typeid']]

        feature_array.append(features)
        target_array.append(vote['typeid'])

    return (feature_array, target_array)



def sklearn_classifier_score(features,targets):

#   gnb = GaussianNB()
    svm = SVC()

    features = [[float(number) for number in feature] for feature in features]

    train_features  = np.array(features[len(features)/2:])
    train_targets   = np.array(targets[len(targets)/2:])
    test_features   = np.array(features[:len(features)/2])
    test_targets    = np.array(targets[:len(targets)/2])

    classifier = svm.fit(train_features, train_targets)

    return svm.score(test_features, test_targets)



def sklearn_classifier_Kfold_score(features,targets):

#   gnb = GaussianNB()
    svm = SVC()

    features = [[float(number) for number in feature] for feature in features]

    features    = np.array(features)
    targets     = np.array(targets)

    K = 40

    cv = cross_validation.KFold(len(targets), n_folds=K, indices=False)
    
    accuraccies = []

    for train_index, test_index in cv:
        train_features  = np.array(features[train_index])
        train_targets   = np.array(targets[train_index])
        test_features   = np.array(features[test_index])
        test_targets    = np.array(targets[test_index])

        classifier = svm.fit(train_features, train_targets)

        accuraccies.append(svm.score(test_features, test_targets))


    return sum(accuraccies)/len(accuraccies)
    


#data_tuple  = get_MP_classifier_data_sklearn(5)
#features    = data_tuple[0]
#features    = data_tuple[0]
#print sklearn_classifier_K_fold(features, targets)

















