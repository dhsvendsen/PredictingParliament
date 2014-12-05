# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import urllib, json
import pickle
import resume_lda
import HTMLParser
import odaparsers
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import os

def index(request):
	return render(request, 'query_folketinget/index.html')

def test(request):
	url = "http://oda.ft.dk/api/Afstemning?$inlinecount=allpages"
	response = urllib.urlopen(url);
	data = json.loads(response.read())
	data_return = json.dumps(data)
	oda = data['odata.metadata']
	context = {'data' : data_return}
	return HttpResponse(data_return)

def predict(request):
    h = HTMLParser.HTMLParser()
    parties  = ['Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
                'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
                'Liberal Alliance', 'Det Konservative Folkeparti']
    categories =  ['Beretning af almen art','Alm. del','FT','Henvendelser uden bilagsnummer',
                   'Mødesag','Info-noter','US','Alm. del §-markeret','EU-noter',
                   'B1 - Privat forslag - 1. (eneste) beh.','S','Privat forslag','Regeringsforslag','B3',
                   'B1 - Privat forslag','B2','B1 - Regeringsforslag']
    title = request.POST['title']
    proposals = ['Beslutningsforslag', 'Lovforslag']
    proposing_party = request.POST["proposing_party"]
    p_party_input = [1 if e==proposing_party  else 0 for e in parties]
    case_category = request.POST['case_category']
    c_category_input = [1 if e ==h.unescape(case_category) else 0 for e in categories]
    proposal_type = request.POST['proposal_type']
    p_type_input = [1 if e==proposal_type else 0 for e in proposals]
    summary = request.POST["summary"]
    p_party_input.extend(c_category_input)
    p_party_input.extend(p_type_input)
    #ones_list = temp_ones_list.extend(p_type_input)
    #with open('classifier_294.pkl')
    text_input = title + " " + summary
    topic_array = resume_lda.lda_topics(text_input)
    p_party_input.extend(topic_array)
#    print c_category_input
    print p_party_input
    print len(p_party_input)
    data_object = np.array(p_party_input)
    
    all_mp = [(dicts['id'],dicts['navn']) for dicts in odaparsers.all_MPs()]     
    DecisionTreeClassifier(max_depth=5)
     
    predictions = []
     
    for mp in all_mp:
        classifier_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'decisiontrees/classifier_{0}.pkl'.format(mp[0]))
        try:
            with open(classifier_path, 'rb') as in_file:
                print in_file
                dtc = pickle.load(in_file)
            predictions.append((mp[1], dtc.predict(data_object)[0]))
        except IOError:
            print 'Actor of id {0} is not an actively voting MP'.format(mp[0]) 
    print predictions
    print type(predictions)
    #data_return = json.loads(predictions)
    context = {'votes' : predictions}
    #html = render_to_string('wishit/show_predictions.html', context)
    #return HttpResponse(html, mimetype='application/javascript')
    return HttpResponse("JEPS")

"""
def test(request):
	url = "http://oda.ft.dk/api/Afstemning?$inlinecount=allpages"
	response = urllib.urlopen(url);
	data = json.loads(response.read())
	data_return = json.dumps(data)
	oda = data['odata.metadata']
	context = {'data' : data_return}
	return HttpResponse(data_return)
"""
