# -*- coding: utf-8 -*-

"""This submodule deals with everything related to the parliament database.

The parliament database is distributed and maintained by the Danish Parliament.
It is made available using the Open Data Protocol (Odata) which allows non
associated persons to freely query the database using a url query language. 
The database is made available at oda.ft.dk.
"""

import requests as rq
import json
import os

PARENTDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, PARENTDIR)


class OdaGetter:

    """Retrieve data from the parliament database.

    This class is strictly related to retrieving data from the parliament
    database through Odata.
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
        """Return actors in parliament.

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
             {
              "typeid": 5, 
              "periodeid": null, 
              "startdato": null, 
              "biografi": "<?xml version=\"1.0\" encoding=\"utf-16\"?>(...)", 
              "gruppenavnkort": null, 
              "opdateringsdato": "2014-09-11T17:59:38.67", 
              "slutdato": null, 
              "navn": "Frank Aaen", 
              "efternavn": "Aaen", 
              "fornavn": "Frank", 
              "id": 5
             },
             ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Aktør?$filter=typeid eq 5'
        self.filename = 'aktoer'

        return self.odata_with_db(self.url, self.filename)


    def get_stemme(self, aktoerid):
        """Return all votes cast by a member of parliament (MP).

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
             {
              "typeid": 1, 
              "akt\u00f8rid": 5, 
              "afstemningid": 1, 
              "id": 53, 
              "opdateringsdato": "2014-09-09T09:05:59.653"
             }, 
             ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Stemme?$filter=aktørid'\
            'eq {0}'.format(aktoerid)
        self.filename = 'stemme%d' % aktoerid

        return self.odata_with_db(self.url, self.filename)


    def get_afstemning(self):
        """Return all parliamentary votes in parliament.

        Uses 'odata_with_db' to retrieve a list of all parliamentary votes
        in parliament.

        Returns
        -------
        out : data-list
            List-type JSON readable dataset.

            Example
            -------
            [
             {
              "vedtaget": true, 
              "typeid": 2, 
              "nummer": 411, 
              "sagstrinid": null, 
              "opdateringsdato": "2014-09-09T09:05:59.653", 
              "m\u00f8deid": 17, 
              "konklusion": "Vedtaget\n\n108 stemmer for (...)", 
              "id": 1, 
              "kommentar": null
             }, 
             ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Afstemning'
        self.filename = 'afstemning'

        return self.odata_with_db(self.url, self.filename)


    def get_sag(self, sagid):
        """Return a specific case.

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
            {
             "periodeid": 32, 
             "titel": "Forslag til lov om \u00e6ndring af (...)", 
             "afg\u00f8relsesdato": null, 
             "afstemningskonklusion": "Vedtaget\n\n98 stemmer (...)", 
             "retsinformationsurl": null, 
             "paragraf": "", 
             "nummernumerisk": "200", 
             "id": 1449, 
             "nummerpostfix": "", 
             "begrundelse": "", 
             "fremsatundersagid": null, 
             "opdateringsdato": "2014-09-26T12:32:36.103", 
             "statsbudgetsag": true, 
             "lovnummerdato": null, 
             "statusid": 11, 
             "nummerprefix": "L", 
             "afg\u00f8relsesresultatkode": "", 
             "paragrafnummer": null, 
             "deltundersagid": null, 
             "kategoriid": 13, 
             "lovnummer": "992", 
             "resume": "Lovforslaget \u00e6ndrer (...)", 
             "odata.metadata": "http://oda.ft.dk/api/(...)", 
             "offentlighedskode": "O", 
             "baggrundsmateriale": null, 
             "titelkort": "Om indgreb mod utilsigtet udnyttelse (...)", 
             "typeid": 3, 
             "nummer": "L 200", 
             "afg\u00f8relse": "", 
             "r\u00e5dsm\u00f8dedato": null
            }
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
        """Return all ministries in parliament.

        Uses 'odata_with_db' to retrieve a list of all ministries in
        parliament.

        Returns
        -------
        out : data-list

            Example
            -------
            [
             {
              "typeid": 1, 
              "periodeid": null, 
              "startdato": null, 
              "biografi": "", 
              "gruppenavnkort": null, 
              "opdateringsdato": "2014-11-14T11:38:35.957", 
              "slutdato": null, 
              "navn": "Finansministeriet", 
              "efternavn": null, 
              "fornavn": "Finansministeriet", 
              "id": 2
             },
             ...
            ]
        """
        self.url = 'http://oda.ft.dk/api/Aktør?$filter=typeid eq 1'
        self.filename = 'ministeromraaede_aktoer'

        return self.odata_with_db(self.url, self.filename)


    def get_sagstrin(self, sagstrinid):
        """Return case stage (da: 'sagstrin').

        Uses 'odata' to retrieve a dictionary object with case stage
        data for a parliamentary vote. Is used to get the 'sagid' (en: caseid).

        Parameters
        ----------
        sagstrinid : id-integer
            Int-type case stage id.

        Returns
        -------
        out : case-level-dict
            Dictionary containing information about a case stage.

            Example
            -------
            {
             "typeid": 17, 
             "folketingstidendesidenummer": "", 
             "titel": "Eventuelt: 3. behandling", 
             "opdateringsdato": "2014-11-07T13:01:55.26", 
             "odata.metadata": "http://oda.ft.dk/api/(...)",
             "folketingstidendeurl": "", 
             "sagid": 1449, 
             "statusid": 41, 
             "dato": "2014-09-09T09:15:00", 
             "folketingstidende": "F", 
             "id": 4849
            }
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
