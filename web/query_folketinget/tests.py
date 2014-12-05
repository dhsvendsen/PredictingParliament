# -*- coding: utf-8 -*-
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('query_folketinget:index'))
        self.assertEqual(response.status_code, 200)

    def test_predict(self):
        response = self.client.post(
            reverse('query_folketinget:predict'),
            {
                'title': 'undervisning',
                'proposing_party': 'Dansk Folkeparti',
                'case_category': 'Beretning af almen art',
                'proposal_type': 'Beslutningsforslag',
                'summary': 'Indvandrere i storkøbenhavn skal have bedre \
                forudsætninger for at lære godt dansk'
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['votes']), 178)
