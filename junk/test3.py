import main
from OdaGetter import *

getter = OdaGetter()

def get_MP_resumes(aktoerid):
    """
        Returns a list of tuples, each representing a datapoint for the classifier.
        Example [({FEATURES}, yes), 
                 ({FEATURES}, no), 
                 ({FEATURES}, no), ...]
    """
    resume = []
    votings=getter.get_afstemning()
    for i, vote in enumerate(main.get_MP_votes(aktoerid)):
        if not votings[i]['typeid'] == 1:
            continue
        case = main.get_case(vote['afstemningid'])
        resume.append(case['resume'])
    
    return list(set(resume))

print get_MP_resumes(5)