# -*- coding: utf-8 -*-

"""This submodule deals with everything related to the parliament database.

The parliament database is distributed and maintained by the Danish Parliament.
It is made available using the Open Data Protocol (Odata) which allows non
associated persons to freely query the database using a url query language.
The database is made available at www.oda.ft.dk.
"""

import requests as rq
import json
import os

PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)


class OdaGetter(object):

    """Retrieve data from the parliament database.

    This class is strictly related to retrieving data from the parliament
    database through the Open Data Protocol (Odata). The database can be found
    at www.oda.ft.dk.
    """

    @classmethod
    def _write_to_database(cls, data, filename):
        """Write data to file and return nothing."""
        with open(PARENTDIR + '/storing/database/%s.txt' % filename,
                  'w') as out_data:
            out_data.write(json.dumps(data, indent=1))

    @classmethod
    def _read_from_database(cls, filename):
        """Return data from file in 'storing/database'."""
        with open(PARENTDIR + '/storing/database/%s.txt' % filename,
                  'r') as in_data:
            return json.load(in_data)

    def odata_with_db(self, url, filename=None):
        """Return dataset either by loading locally or retrieving and storing.

        Parameters
        ----------
        url : url-string
            Str-type query url, specifying the wanted dataset. Must be
            constructed in accordance to the syntax rules specified at
            http://www.odata.org/documentation.

        filename : filename-string
            Str-type filename that the method should read from/write to.
            Defaults to final part of url-string seperated by '/'.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset.
        """
        if filename is None:
            filename = url.split('/')[-1]

        try:
            return self._read_from_database(filename)
        except IOError:
            self.data = rq.get(url).json()

            try:
                self.nextlink = self.data['odata.nextLink']
            except KeyError:
                self._write_to_database(self.data, filename)
                return self.data

            self.new_data = self.data
            self.data = self.data['value']

            while True:
                if 'odata.nextLink' in self.new_data:
                    self.nextlink = self.new_data['odata.nextLink']
                    self.new_data = rq.get(self.nextlink).json()
                    self.data.extend(self.new_data['value'])
                else:
                    break

            self._write_to_database(self.data, filename)
            print "Writing to database"

            return self.data

    def odata(self, url):
        """Return dataset by retieving through Odata, without storing.

        A very simple version of 'odata_with_db' that retrieved without
        loading from or storing to a local database.

        Parameters
        ----------
        url : url-string
            Str-type query url, specifying the wanted dataset.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset.
        """
        self.data = rq.get(url).json()

        return self.data

    def get_aktoer(self):
        r"""Return actors in parliament.

        Uses 'odata_with_db' to retrieve a list of data for each actor in the
        parliament. This include any person or group that the parliament
        interacts with on record.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset.

            Example
            -------
            [
             {u'biografi': u'<?xml version="1.0" encoding="utf-16"?>(...)',
              u'efternavn': u'Aaen',
              u'fornavn': u'Frank',
              u'gruppenavnkort': None,
              u'id': 5,
              u'navn': u'Frank Aaen',
              u'opdateringsdato': u'2014-09-11T17:59:38.67',
              u'periodeid': None,
              u'slutdato': None,
              u'startdato': None,
              u'typeid': 5},
             ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Aktør?$filter=typeid eq 5'
        self.filename = 'aktoer'

        return self.odata_with_db(self.url, self.filename)

    def get_stemme(self, aktoerid):
        r"""Return all votes cast by a member of parliament (MP).

        Uses 'odata_with_db' to retrieve a list of all votes the a given MP
        has cast. 'Returns' is not specified below as this is explained in
        'odata_with_db'.

        Parameters
        ----------
        aktoerid : id-integer
            Int-type corresponding to the actor-id with which the members of
            parliament are indexed on www.oda.ft.dk.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset.

            Example
            -------
            [
             {u'afstemningid': 1,
              u'akt\xf8rid': 5,
              u'id': 53,
              u'opdateringsdato': u'2014-09-09T09:05:59.653',
              u'typeid': 1},
              ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Stemme?$filter=aktørid'\
            'eq {0}'.format(aktoerid)
        self.filename = 'stemme%d' % aktoerid

        return self.odata_with_db(self.url, self.filename)

    def get_afstemning(self):
        r"""Return all parliamentary votes in parliament.

        Uses 'odata_with_db' to retrieve a list of all parliamentary votes
        in parliament.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset.

            Example
            -------
            [
             {u'afstemningid': 792,
              u'akt\xf8rid': 5,
              u'id': 753,
              u'opdateringsdato': u'2014-09-19T14:41:03',
              u'typeid': 3},
              ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Afstemning'
        self.filename = 'afstemning'

        return self.odata_with_db(self.url, self.filename)

    def get_sag(self, sagid):
        r"""Return a specific case.

        Uses 'odata_with_db' to retrieve a dictionary object with information
        about a specific case.

        Parameters
        ----------
        sagid : id-integer
            Int-type case ID. The danish word 'Sag' translates to 'case' in
            english.

        Returns
        -------
        out : case-dictionary
            Dict-type object that holds information about a specific case
            that has been/is to be voted on in parliament.

            Example
            -------
            {u'afg\xf8relse': u'',
             u'afg\xf8relsesdato': None,
             u'afg\xf8relsesresultatkode': u'',
             u'afstemningskonklusion': u'Vedtaget\n\n111 stemmer for (...)',
             u'baggrundsmateriale': None,
             u'begrundelse': u'',
             u'deltundersagid': None,
             u'fremsatundersagid': None,
             u'id': 69,
             u'kategoriid': 13,
             u'lovnummer': u'306',
             u'lovnummerdato': None,
             u'nummer': u'L 107',
             u'nummernumerisk': u'107',
             u'nummerpostfix': u'',
             u'nummerprefix': u'L',
             u'odata.metadata': u'http://oda.ft.dk/api/%24metadata#Sag/(...)',
             u'offentlighedskode': u'O',
             u'opdateringsdato': u'2014-09-12T20:00:31.7',
             u'paragraf': u'',
             u'paragrafnummer': None,
             u'periodeid': 32,
             u'resume': u'Loven om Danmarks Innovationsfond bygger (...)',
             u'retsinformationsurl': None,
             u'r\xe5dsm\xf8dedato': None,
             u'statsbudgetsag': True,
             u'statusid': 11,
             u'titel': u'Forslag til lov om Danmarks Innovationsfond.',
             u'titelkort': u'Om Danmarks Innovationsfond.',
             u'typeid': 3}
        """
        self.url = 'http://oda.ft.dk/api/Sag(%d)' % sagid
        self.filename = 'sag' + str(sagid)

        return self.odata_with_db(self.url, self.filename)

    def get_lb_sager(self):
        """Return all cases that are either bills or motions.

        Uses 'odata_with_db' to retrieve a list of all cases of type L or B.
        Bills (da: 'lovforslag') has numberprefix (da: 'nummerprefix') 'L'.
        Motions (da: 'beslutningsforslag') has numberprefix 'B'. This method
        returns a list containing all of these, for later use in submodule
        classification.resume_lda.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset, each element in which has the
            same form as the output of function 'get_sag'.
        """
        self.url = "http://oda.ft.dk/api/Sag?$filter=nummerprefix eq 'L' or"\
            " nummerprefix eq 'B'"
        self.filename = 'LB_sager'

        return self.odata_with_db(self.url, self.filename)

    def get_ministeromraaede_aktoer(self):
        r"""Return all ministries in parliament.

        Uses 'odata_with_db' to retrieve a list of all ministries in
        parliament.

        Returns
        -------
        out : data-list

            Example
            -------
            [
             {u'biografi': u'',
              u'efternavn': None,
              u'fornavn': u'Finansministeriet',
              u'gruppenavnkort': None,
              u'id': 2,
              u'navn': u'Finansministeriet',
              u'opdateringsdato': u'2014-11-14T11:38:35.957',
              u'periodeid': None,
              u'slutdato': None,
              u'startdato': None,
              u'typeid': 1},
              ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Aktør?$filter=typeid eq 1'
        self.filename = 'ministeromraaede_aktoer'

        return self.odata_with_db(self.url, self.filename)

    def get_sagstrin(self, sagstrinid):
        """Return case stage (da: 'sagstrin').

        Uses 'odata' to retrieve a dictionary object with case stage data
        for a parliamentary vote. Is used to get the 'sagid' (en: 'case ID').

        Parameters
        ----------
        sagstrinid : id-integer
            Int-type case stage ID.

        Returns
        -------
        out : case-level-dict
            Dictionary containing information about a case stage.

            Example
            -------
            {u'dato': u'2014-09-09T09:15:00',
             u'folketingstidende': u'F',
             u'folketingstidendesidenummer': u'',
             u'folketingstidendeurl': u'',
             u'id': 4849,
             u'odata.metadata': u'http://oda.ft.dk/api/(...)',
             u'opdateringsdato': u'2014-11-07T13:01:55.26',
             u'sagid': 1449,
             u'statusid': 41,
             u'titel': u'Eventuelt: 3. behandling',
             u'typeid': 17}
        """
        self.url = 'http://oda.ft.dk/api/Sagstrin(%d)' % sagstrinid

        return self.odata(self.url)

    def get_sagaktoer(self, sagid, rolleid):
        """Return ID of actor that occupies a given role in a given case.

        Used to return id of actor that proposed a case (rolleid = 19) or
        ministry that the case originated from (rolleid = 6).

        Parameters
        ----------
        sagid : id-integer
            Int-type case ID.

        rolleid : id-integer
            Int-type role ID (da: 'rolle').

        Returns
        -------
        out : actor-id
            The ID number of the actor that occied the given role.
        """
        self.url = 'http://oda.ft.dk/api/SagAktør?$filter=sagid eq {0} and'\
            ' rolleid eq {1}'.format(sagid, rolleid)

        return self.odata(self.url)['value'][0][u'akt\xf8rid']
