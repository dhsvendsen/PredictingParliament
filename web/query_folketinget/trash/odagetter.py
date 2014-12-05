# -*- coding: utf-8 -*-

"""This class deals with everything related to the ODA database distributed and
maintained by the Danish Parliament. Each of the functions in this class are
designed to extract a particular JSONs from the database. The functions are
named get_[name of dataset], where [name of dataset] is the resource pulled
from oda.ft.dk.
"""

import requests as rq
import json
import os


class OdaGetter:
    """This class is strictly comprised of methods that retrieve raw data from
    the ODA database at oda.ft.dk.

    Examples
    --------
    >>> getter = OdaGetter()
    >>> actors = getter.get_aktoer()
    >>> type(actors) == list
    True
    """

    def __write_to_database__(self, data, filename):
        """Writes data to filename and returns nothing.
        """

        GDRAT_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'database/LB_sager.txt')
        with open(GDRAT_abs_path, 'w') as out_data:
            out_data.write(json.dumps(data, indent=1))

    def get_odata_with_db(self, url, filename=None):
        """Takes an ODA query url as argument and returns the result, storing
        it to the databse if it cannot be readily retrieved from it.
        """
        if filename is None:
                filename = url.split('/')[-1]

        try:
            with open('database/%s.txt' % filename, 'r') as in_data:
                return json.load(in_data)
        except IOError:
            self.data = rq.get(url).json()

            try:
                self.nextLink = self.data['odata.nextLink']  # Store
            except KeyError:
                self.__write_to_database__(self.data, filename)
                return self.data

            self.new_data = self.data
            self.data = self.data['value']

            while True:
                if 'odata.nextLink' in self.new_data:
                    self.nextLink = self.new_data['odata.nextLink']
                    self.new_data = rq.get(self.nextLink).json()
                    self.data.extend(self.new_data['value'])
                else:
                    break

            self.__write_to_database__(self.data, filename)
            print "Writing to database"

            return self.data

    def get_odata(self, url):
        """Takes an ODA query url as argument and returns the result without
        storing it to the database. This method is only made for retrieving
        single page datasets.
        """
        self.data = rq.get(url).json()

        return self.data

    def get_aktoer(self):
        """Return a list with an entry for each actor of typeid 5, i.e. humans
        that have interacted with the parliament. 'Aktoer' translates to actor.
        """
        self.url = 'http://oda.ft.dk/api/Aktør?$filter=typeid eq 5'
        self.filename = 'aktoer'

        return self.get_odata_with_db(self.url, self.filename)

    def get_stemme(self, aktoerid):
        """Return a list containing information about all votes a particular
        politician has cast.
        """
        self.url = 'http://oda.ft.dk/api/Stemme?$filter=aktørid eq {0}'.format(aktoerid)
        self.filename = 'stemme%d' % aktoerid

        return self.get_odata_with_db(self.url, self.filename)


    def get_afstemning(self):
        """Return a list containing information about all votes in parliament.
        """
        self.url = 'http://oda.ft.dk/api/Afstemning'
        self.filename = 'afstemning'

        return self.get_odata_with_db(self.url, self.filename)


    def get_sag(self, sagid):
        """Returns a JSON that contains information about a particular case.
        """
        self.url = 'http://oda.ft.dk/api/Sag(%d)' % sagid
        self.filename = 'sag' + str(sagid)

        return self.get_odata_with_db(self.url, self.filename)


    def get_LB_sager(self):
        """Returns a JSON containing all cases with number-prefixes L and B.
        """
        self.url = "http://oda.ft.dk/api/Sag?$filter=nummerprefix eq 'L' or nummerprefix eq 'B'"
        self.filename = 'LB_sager'

        return self.get_odata_with_db(self.url, self.filename)


    def get_ministeromraaede_aktoer(self):
        """Returns a list with an entry for each ministry in parliament.
        """
        self.url = 'http://oda.ft.dk/api/Aktør?$filter=typeid eq 1'
        self.filename = 'ministeromraaede_aktoer'

        return self.get_odata_with_db(self.url, self.filename)


    def get_sagstrin(self, sagstrinid):
        """Returns a JSON array of 1 element that is used to get the "sagid" 
        i.e. the case-id. Albeit the simplest way to get the case-id, it is a 
        cumbersome one.
        """
        self.url = 'http://oda.ft.dk/api/Sagstrin(%d)' % sagstrinid

        return self.get_odata(self.url)


    def get_sagaktoer(self, sagid, rolleid):
        """Returns id of actor that proposed a case (rolleid = 19) or is the
        ministry that the case originated from (rolleid = 6).
        """
        self.url = 'http://oda.ft.dk/api/SagAktør?$filter=sagid eq {0} and rolleid eq {1}'.format(sagid,rolleid)

        return self.get_odata(self.url)['value'][0][u'akt\xf8rid']




