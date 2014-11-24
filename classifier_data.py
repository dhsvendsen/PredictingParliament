from OdaParser import *
from resume_lda_modified import *
import xml.etree.ElementTree as ET

## --> Each of the below functions return a zero-array which holds a single 1
## ... representing the precense of a feature in a case (observation). These 
## ... arrays are combined into a full X matrix in the final part of this sript.
## ... Note that in some cases a feature may not be present for an observation, 
## ... in which case the function will just return the zero-array. Full rows of
## ... zeros, i.e. features that were never present will be deleted in the
## ... final step of this script.


def feat_party(caseid):
    """
        Returns feature array representing the party of the proposing MP (PMP).
    """

    parties  = ['Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
                'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
                'Liberal Alliance', 'Det Konservative Folkeparti']

    try:
        aktoerid = getter.get_sagaktoer(caseid,19) #19 is the typeid for pyth
    except IndexError:
        print "No actor with role id 19 was found for caseid %d. Returning 0-array." % caseid
        return np.zeros(len(parties))

    data = single_MP(aktoerid)
    #data = json.loads(data)

    try:
        root = ET.fromstring(data['biografi'].encode('utf-16'))
    except:
        print "No info ('biografi') was found for MP: %s. Returning 0-array." % aktoerid
        return np.zeros(len(parties))

    party    = root.find('party').text

    feat_array = np.zeros(len(parties))

    for i, p in enumerate(parties):
        if party == p:
            feat_array[i] = 1
            break
    else:
        print "No party was found for caseid: %d. Returning 0-array." % caseid

    return feat_array



def feat_ministry(caseid):
    """
        Returns feature array representing the ministry of origin (MOO) of the
        proposition.
    """

    ministries = [n['navn'] for n in getter.get_ministeromraaede_aktoer()]

    try:
        aktoerid = getter.get_sagaktoer(caseid,6) #6 is the typeid for MOO
    except IndexError:
        print "No actor with role id 6 was found for caseid %d. Returning 0-array." % caseid
        return np.zeros(len(ministries))

    data     = single_PMP(aktoerid)
    ministry = data['navn']

    feat_array = np.zeros(len(ministries))
    
    for i, m in enumerate(ministries):
        if ministry == m:
            feat_array[i] = 1
            break
    else:
        print "No ministry was found for caseid: %d. Returning 0-array." % caseid

    return feat_array



def feat_category(case_categoryid):
    """
        Returns feature array representing the category of the proposition.
    """
    feat_array = np.zeros(17) # There are 17 different categories
    feat_array[case_categoryid-1] = 1

    return feat_array



def feat_L_or_B(case_nummerprefix):
    """
        Returns feature array representing whether proposition is bill (L) or 
        motion (B).
    """
    if case_nummerprefix == 'L':
        return np.array([1., 0.])
    elif case_nummerprefix == 'B':
        return np.array([0., 1.])
    else:
        return np.array([0., 0.])



def feat_party_votes(case_afstemningskonklusion):
    """Return feature array representing what parties votes yes (1) for the
    proposition, and what parties voted no (0).
    """
    parties = ['S','RV','SF','EL','LA','V','DF','KF','UGF']
    feat_array = np.zeros(len(parties))

    try:
        parties_for = re.search("\(.*?\)", case_afstemningskonklusion).group(0)
    except:
        print "No ('afstemningskonklusion') was found for caseid %d. Returning 0-array."
        return np.zeros(len(parties))

    for index, party in enumerate(parties):
        if party in parties_for:
            feat_array[index] = 1

    return feat_array



def feat_title_length(case_titel):
    return len(case_titel)

def feat_resume_length(case_resume):
    return len(case_resume)


## --> Below we combile the 'feat_'-functions above into a full X matrix, that is
## ... to be interpreted by an SVM classifier.


def remove_zero_cols(X):
    """
    Takes a numpy array or matrix and removes coloumns that consist only of zeros
    """
    zero_cols = []
    for i in range( X.shape[1] ):
        if sum(X[:,i]) == 0:
            zero_cols.append(i)
        
    X=np.delete(X,zero_cols,1)
    return X


def dataset_X_y(aktoerid):
    """
        Returns a clean dataset X of features for every case the given MP has
        voted in, along with a target vector y, representing his/her vote in
        said case.
    """

    # Get list of votes that the given MP has cast
    MP_votes_list  = MP_votes(aktoerid) # VIRKER. RETURNERER LISTE MED FORSKELLIGE AFSTEMNINGID

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

    X = []
    y = []
    for MP_vote in MP_votes_list:

        # Check if vote is final, i.e. typeid = 1
        continue_after_check = True
        for vote in all_votes_list:
            if MP_vote['afstemningid'] == vote['id']:
                if vote['typeid'] != 1:
                    continue_after_check = False
                    print "Vote not final"
                    break

        if continue_after_check == False:
            continue


        # Instantiate case profile to extract features from
        case = vote_case(MP_vote['afstemningid'])

        if case['id'] in processed_cases:
            print "Dublicate found! Vote %d in case %d" % (MP_vote['afstemningid'], case['id'])
            continue
        else:
            processed_cases.append(case['id'])


        print "\nProcessing vote %d in case %d - MP id %d\n" % (MP_vote['afstemningid'], case['id'], aktoerid)

        X_case = []

        X_case.extend(feat_party(case['id']))
        print "Successfully added party\t to features for caseid\t %d" % case['id']

        #X_case.extend(feat_ministry(case['id']))
        #print "Successfully added ministry\t to features for caseid\t %d" % case['id']

        X_case.extend(feat_category(case['kategoriid']))
        print "Successfully added category\t to features for caseid\t %d" % case['id']

        X_case.extend(feat_L_or_B(case['nummerprefix']))
        print "Successfully added numberprefix\t to features for caseid\t %d" % case['id']

        X_case.extend(lda_topics(case['resume']))
        print "Successfully added LDA topics\t to features for caseid\t %d" % case['id']

        #X_case.extend(feat_party_votes(case['afstemningskonklusion']))
        #print "Successfully added party votes\t to features for caseid\t %d" % case['id']

        #X_case.append(feat_title_length(case['titel']))
        #print "Successfully added title length\t to features for caseid\t %d" % case['id']

        #X_case.append(feat_resume_length(case['resume']))
        #print "Successfully added resume length to features for caseid\t %d" % case['id']

        X.append(X_case)
        y.append(MP_vote['typeid'])

    return np.array(X), np.array(y)#remove_zero_cols(np.array(X)), np.array(y)



