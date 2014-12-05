#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script includes the main function of the program.

It calls the dataset_X_y from classification.classifier_data to generate a data
matrix and class index for each member of parliament and subsequently trains a
decision tree classifier - the classifier found to be most effective. Data
matrices and classifiers are saved to .npy and .pkl files respectively.

Usage: 
    python generate_classifiers.py [-f | --force]

Options: 
    -f --force  generate classifiers based on all new datamatrices by forcing
                program to overwrite existing data.
"""

import classification.classifier_data as cd
import dataretrieval.odaparsers as opa
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import pickle
import sys


def main(force=False):
    """Generate and store datamatrices and classifiers for all MPs."""
    _all_mps = [dicts['id'] for dicts in opa.all_mps()]

    for mp_id in _all_mps:
        X, y = cd.dataset_X_y(mp_id, force=force)

        np.save('storing/matrices/X_{0}'.format(mp_id), X)
        np.save('storing/matrices/y_{0}'.format(mp_id), y)

        if X.size == 0:
            print 'Actor of id {0} is not an active member of the'\
                  'parliament'.format(mp_id)
        else:
            dtc = DecisionTreeClassifier(max_depth=5).fit(X, y)
            write_path = 'storing/classifiers/classifier_{0}.pkl'.format(mp_id)
            with open(write_path, 'wb') as out_file:
                pickle.dump(dtc, out_file)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    _force = arguments['--force']
    print _force
    sys.exit()

    if _force:
        main(force=True)
    else:
        main()
