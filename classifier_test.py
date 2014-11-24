from classifier_data import *
from sklearn.ensemble import RandomForestClassifier


def sklearn_classifier_score(features,targets):

    gnb = GaussianNB()
#    svm = SVC()

    features = [[float(number) for number in feature] for feature in features]

    train_features  = np.array(features[len(features)/2:])
    train_targets   = np.array(targets[len(targets)/2:])
    test_features   = np.array(features[:len(features)/2])
    test_targets    = np.array(targets[:len(targets)/2])

    gnb.fit(train_features, train_targets)

    return svm.score(test_features, test_targets)



def classifier_score(features,targets):

#   gnb = GaussianNB()
#   svm = SVC()
    
    cla = DecisionTreeClassifier()

    K = 10

    cv = cross_validation.StratifiedKFold(targets, n_folds=K, indices=False)
    
    accuraccies = []

    for train_index, test_index in cv:
        train_features  = np.array(features[train_index])
        train_targets   = np.array(targets[train_index])
        test_features   = np.array(features[test_index])
        test_targets    = np.array(targets[test_index])

        cla.fit(train_features, train_targets)

        accuraccies.append(cla.score(test_features, test_targets))

    cla.fit(features,targets)

    print cla.predict(features)


    return sum(accuraccies)/len(accuraccies)


def classifier_score_rf(features,targets):

#   gnb = GaussianNB()
#   svm = SVC()
    
    cla = RandomForestClassifier(n_estimators=500)

    K = 10

    cv = cross_validation.StratifiedKFold(targets, n_folds=K, indices=False)
    
    accuraccies = []

    for train_index, test_index in cv:
        train_features  = np.array(features[train_index])
        train_targets   = np.array(targets[train_index])
        test_features   = np.array(features[test_index])
        test_targets    = np.array(targets[test_index])

        cla.fit(train_features, train_targets)

        accuraccies.append(cla.score(test_features, test_targets))

    cla.fit(features,targets)

    print cla.predict(features)


    return sum(accuraccies)/len(accuraccies)


#data_tuple  = get_MP_classifier_data_sklearn(5)
#features    = data_tuple[0]
#features    = data_tuple[0]
#print sklearn_classifier_K_fold(features, targets)



