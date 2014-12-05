import odaparsers
import os
import pickle

def predict_votes(data_object):
    """Predict the votes of the politicians
    """
    predictions = []
    all_mp = [(dicts['id'], dicts['navn']) for dicts in odaparsers.all_MPs()]
    for mp in all_mp:
        classifier_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'decisiontrees/classifier_{0}.pkl'.format(mp[0])
        )
        try:
            with open(classifier_path, 'rb') as in_file:
                #print in_file
                dtc = pickle.load(in_file)
            predictions.append((mp[1], dtc.predict(data_object)[0]))
        except IOError:
            print 'Actor of id {0} is not an actively voting MP'.format(mp[0])
    return predictions

