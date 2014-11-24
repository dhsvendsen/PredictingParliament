from OdaParser import *
import xml.etree.ElementTree as ET

## FUNCTIONS THAT RETURN ARRAYS TO BE COMBPILED INTO A FULL X MATRIX

def feat_case_party(caseid):
    """
        Returns feature array representing the party of the proposing MP.
    """

    parties	 = ['Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
    			'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
    			'Liberal Alliance', 'Det Konservative Folkeparti']

    try:
    	aktoerid = getter.get_sagaktoer(caseid,19) #19 is the typeid for propositioner
    except IndexError:
    	return np.zeros(len(parties))

    data     = getter.get_aktoer_from_id(aktoerid).text
    data 	 = json.loads(data)
    root	 = ET.fromstring(data['biografi'].encode('utf-16'))
    party 	 = root.find('party').text

    feat_array = np.zeros(len(parties))

    for i, p in enumerate(parties):
    	if party == p:
    		feat_array[i] = 1
    		break
    else:
    	print "Warning: No party was found for caseid: %d. Returning array of zeros." % caseid

    return feat_array



def feat_case_ministry(caseid):
	"""
		Returns feature array representing the ministry of the proposition.
	"""

	ministries = [ n['navn'] for n in getter.get_ministeromraaede_aktoer() ]

	try:
		aktoerid = getter.get_sagaktoer(caseid,6) #6 is the typeid for ministry of origin
	except IndexError:
		return np.zeros(len(ministries))

	data     = getter.get_aktoer_from_id(aktoerid).text
	data 	 = json.loads(data)
	ministry = data['navn']

	feat_array = np.zeros(len(ministries))
	
	for i, m in enumerate(ministries):
		if ministry == m:
			feat_array[i] = 1
			break
	else:
		print "Warning: No ministry was found for caseid: %d. Returning array of zeros." % caseid

	return feat_array



def feat_category(category_id):
    """
        Returns "category" feature array to be used for classification,
        taking as input the category-id from a specific case.
    """
    feat_array = np.zeros(17) # As oda.ft.dk distinguishes between 17 "case-categories" 
    feat_array[category_id-1] = 1
    return feat_array



def feat_L_or_B(case_nummerprefix):
	"""
		Returns feature array representing whether case is bill (L) or motion (B).
	"""
    if case_nummerprefix == 'L':
    	return np.array([1., 0.])
    elif case_nummerprefix == 'B':
        return np.array([0., 1.])
    else:
    	return np.array([0., 0.])


def feat_title_length(case_titel):
	return len(case_titel)

def feat_resume_length(case_resume):
	return len(case_resume)