# -*- coding: utf-8 -*-

"""Manage user interaction with webservice.

This submodule manages central aspects of the user's interaction with the
webservice. Each of the functions control website rendering.
"""

from __future__ import division
from os.path import abspath, dirname, join, realpath
import os

PPARENTDIR = dirname(dirname(dirname(abspath(__file__))))
os.sys.path.insert(0, PPARENTDIR)

import classification.resume_lda as rlda
from django.shortcuts import render
from django.http import HttpResponse
import HTMLParser
import numpy as np
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from scipy import stats
import math
import utils
import json


def index(request):
    """Render front page when user enters website.
    """
    return render(request, 'query_folketinget/index.html')


@csrf_protect
def predict(request):
    """Renders front page with vote predictions.

    Takes a url-request and gets predictions from 'utils', then returns an
    HTTP-response with rendered vote predictions.
    """
    html_parser = HTMLParser.HTMLParser()

    parties = [
        'Venstre', 'Socialdemokratiet', 'Socialistisk Folkeparti',
        'Dansk Folkeparti', 'Radikale Venstre', 'Enhedslisten',
        'Liberal Alliance', 'Det Konservative Folkeparti'
        ]

    categories = [
        u'Beretning af almen art', u'Alm. del', u'FT',
        u'Henvendelser uden bilagsnummer', u'Mødesag', u'Info-noter', u'US',
        u'Alm. del §-markeret', u'EU-noter',
        u'B1 - Privat forslag - 1. (eneste) beh.', u'S', u'Privat forslag',
        u'Regeringsforslag', u'B3', u'B1 - Privat forslag', u'B2',
        u'B1 - Regeringsforslag'
        ]

    proposals = ['Beslutningsforslag', 'Lovforslag']
    GDRAT_abs_path = join(dirname(realpath(__file__)), 'party_member.txt')
    with open(GDRAT_abs_path, 'r') as f:
        party_member = json.load(f)
    print party_member
    print type(party_member)

#    with open('party_member.txt', 'r') as infile:
#        party_member = json.load(infile)

    title, proposing_party, case_category, proposal_type, summary = (
        request.POST['title'],
        request.POST["proposing_party"],
        request.POST['case_category'],
        request.POST['proposal_type'],
        request.POST["summary"]
    )

#   Check that fields are filled out
    for s in [title, proposing_party, case_category, proposal_type, summary]:
        if not s:
            context = {'empty_input': True}
            html = render_to_string('query_folketinget/show_predictions.html',
                                    context)
            return HttpResponse(html, content_type='application/javascript')
        else:
            continue

#   The form input is formatted correctly
    input_list, c_category_input, p_type_input = (
        [1 if e == proposing_party else 0 for e in parties],
        [1 if e == html_parser.unescape(case_category) else 0
            for e in categories],
        [1 if e == proposal_type else 0 for e in proposals]
    )
    text_input = title + " " + summary
    topic_array = rlda.lda_topics(text_input)

#   All the input data is combined in one array
    for inp in (c_category_input, p_type_input, topic_array):
        input_list.extend(inp)
    data_object = np.array(input_list)

#   The votes are predicted
    predictions = utils.predict_votes(data_object)
    final = stats.mode([tup[1] for tup in predictions])
    yes_votes = math.floor(final[1][0]/len(predictions)*100)
    no_votes = math.ceil(100-yes_votes)

    context = {'votes': predictions,
               'final': final,
               'yes': yes_votes,
               'no': no_votes}

    html = render_to_string('query_folketinget/show_predictions.html', context)
    return HttpResponse(html, content_type='application/javascript')
