# -*- coding: utf-8 -*-

# This class deals with everything related to the ODA database distributed and
# maintained by the Danish Parliament. Each of the functions in this class are
# designed to extract a particular JSONs from the database. The functions are
# named get_[name of dataset], where [name of dataset] is the resource pulled
# from oda.ft.dk. 

import requests as rq
import json

class OdaGetter:

	def get_aktoer(self):
		"""
			Returns the raw JSON containing information about all actors in
			parliament. These are not only members of parliament (MP), but also
			groups, privat persons and anyone else associated with parliament.
		"""
		try:
			with open('database/aktoer.txt', 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/Akt%C3%B8r?$inlinecount=allpages&$filter=typeid%20eq%205&$skip=0').json(encoding="utf-16")
			self.nextLink = self.data['odata.nextLink'] # Store 
			self.new_data = self.data
			self.data = self.data['value']

			while True:
				if 'odata.nextLink' in self.new_data:
					self.nextLink = self.new_data['odata.nextLink']
					self.new_data = rq.get(self.nextLink).json()
					self.data.extend(self.new_data['value'])
				else:
					break

			with open('database/aktoer.txt', 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data

	def get_stemme(self, aktoerid):
		"""
			Returns the full JSON array containing information about all votes a particular
			a particular politician has cast.
		"""
		try:
			with open('database/stemme%d.txt' % aktoerid, 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/Stemme?$inlinecount=allpages&$filter=akt%C3%B8rid%20eq%20{0}&$skip=0'.format(aktoerid)).json()
			self.nextLink = self.data['odata.nextLink'] # Store 
			self.new_data = self.data
			self.data = self.data['value']

			while True:
				if 'odata.nextLink' in self.new_data:
					self.nextLink = self.new_data['odata.nextLink']
					self.new_data = rq.get(self.nextLink).json()
					self.data.extend(self.new_data['value'])
				else:
					break

			with open('database/stemme%d.txt' % aktoerid, 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data


	def get_afstemning(self):
		"""
			Returns the full JSON array containing information about all votes.
		"""
		try:
			with open('database/afstemning.txt', 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/Afstemning?$inlinecount=allpages&$skip=0').json()
			self.nextLink = self.data['odata.nextLink'] # Store 
			self.new_data = self.data
			self.data = self.data['value']

			while True:
				if 'odata.nextLink' in self.new_data:
					self.nextLink = self.new_data['odata.nextLink']
					self.new_data = rq.get(self.nextLink).json()
					self.data.extend(self.new_data['value'])
				else:
					break

			with open('database/afstemning.txt', 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data


	def get_sagstrin(self, sagstrinid):
		"""
			Returns a JSON array of 1 element that is used to get the "sagid" i.e. the case-id.
			It is a cumbersome way to get the case-id, however also the only one.
		"""
		self.data = rq.get('http://oda.ft.dk/api/Sagstrin(%d)' % sagstrinid).json()

		return self.data

	def get_sag(self, sagid):
		"""
			Returns a JSON that contains information about a particular case.
		"""
		try:
			with open('database/sag%d.txt' % sagid, 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/Sag(%d)' % sagid).json()

			with open('database/sag%d.txt' % sagid, 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data
   
   
	def get_LB_sager(self):
		"""
			Returns a JSON containing all cases with number-prefixes L and B.
		"""
		try:
			with open('database/LB_sager.txt', 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/Sag?$inlinecount=allpages&$filter=nummerprefix%20eq%20%27L%27').json()
			self.nextLink = self.data['odata.nextLink'] # Store 
			self.new_data = self.data
			self.data = self.data['value']

			while True:
				if 'odata.nextLink' in self.new_data:
					self.nextLink = self.new_data['odata.nextLink']
					self.new_data = rq.get(self.nextLink).json()
					self.data.extend(self.new_data['value'])
				else:
					break
  
			self.nextLink = 'http://oda.ft.dk/api/Sag?$inlinecount=allpages&$filter=nummerprefix%20eq%20%27B%27' 
			self.new_data = rq.get(self.nextLink).json()
   
			while True:
				if 'odata.nextLink' in self.new_data:
					self.nextLink = self.new_data['odata.nextLink']
					self.new_data = rq.get(self.nextLink).json()
					self.data.extend(self.new_data['value'])
				else:
					break
 
			with open('database/LB_sager.txt', 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data


	def get_sagaktoer(self):
		"""
			Returns the full JSON array containing information about all votes.
		"""
		try:
			with open('database/sagaktoer.txt', 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/SagAkt%C3%B8r?$inlinecount=allpages&$skip=0').json()
			self.nextLink = self.data['odata.nextLink'] # Store 
			self.new_data = self.data
			self.data = self.data['value']

			while True:
				if 'odata.nextLink' in self.new_data:
					self.nextLink = self.new_data['odata.nextLink']
					self.new_data = rq.get(self.nextLink).json()
					self.data.extend(self.new_data['value'])
				else:
					break

			with open('database/sagaktoer.txt', 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data 


	def get_sagaktoerrolle(self):
		"""
			Returns the full JSON array containing information about all votes.
		"""
		try:
			with open('database/sagaktoerrolle.txt', 'r') as in_data:
				return json.load(in_data)
		except IOError:
			self.data = rq.get('http://oda.ft.dk/api/SagAkt%C3%B8rRolle?$inlinecount=allpages').json()

			with open('database/sagaktoer.txt', 'w') as out_data:
				out_data.write(json.dumps(self.data,indent=1))

			return self.data 
