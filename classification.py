from OdaParser import *



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

    K = 10

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