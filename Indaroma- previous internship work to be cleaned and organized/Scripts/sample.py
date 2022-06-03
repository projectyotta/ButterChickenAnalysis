# -*- coding: utf-8 -*-
"""
Yelp Fusion API code sample.
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.
Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.
This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.
Sample usage of the program:
`python sample.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import time 


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
	# For Python 3.0 and later
	from urllib.error import HTTPError
	from urllib.parse import quote
	from urllib.parse import urlencode
except ImportError:
	# Fall back to Python 2's urllib2 and urllib
	from urllib2 import HTTPError
	from urllib import quote
	from urllib import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CLIENT_ID = 'A7vIlGtFY6azDIXbDTIJog'
CLIENT_SECRET = '2HTiCJVNXM5fttwTVj9UFI5UKXhHsQOn1iSPHVqCYcTGCJwxIv6e3qQSsHv8P6o1'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


# Defaults for our simple example.
filename_series = '1','2','3','4','5','6','7','8','9','10'
DEFAULT_TERM = 'indian'
DEFAULT_LOCATION ='21682','21683','21684','21685','21686','21687','21688','21690','21701','21702','21703','21704','21705','21709','21710','21711','21713','21714','21715','21716','21717','21718','21719','21720','21721','21722','21723','21727','21733','21734','21737','21738','21740','21741','21742','21746','21747','21748','21749','21750','21754','21755','21756','21757','21758','21759','21762','21765','21766','21767','21769','21770','21771','21773','21774','21775','21776','21777','21778','21779','21780','21781','21782','21783','21784','21787','21788','21790','21791','21792','21793','21794','21795','21797','21798','21801','21802','21803','21804','21810','21811','21813','21814','21817','21821','21822','21824','21826','21829','21830','21835','21836','21837','21838','21840','21841','21842','21843','21849','21850','21851','21852','21853','21856','21857','21861','21862','21863','21864','21865','21866','21867','21869','21871','21872','21874','21875','21890','21901','21902','21903','21904','21911','21912','21913','21914','21915','21916','21917','21918','21919','21920','21921','21922','21930'
SEARCH_LIMIT = 50




def obtain_bearer_token(host, path):
	"""Given a bearer token, send a GET request to the API.
	Args:
		host (str): The domain host of the API.
		path (str): The path of the API after the domain.
		url_params (dict): An optional set of query parameters in the request.
	Returns:
		str: OAuth bearer token, obtained using client_id and client_secret.
	Raises:
		HTTPError: An error occurs from the HTTP request.
	"""
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	assert CLIENT_ID, "Please supply your client_id."
	assert CLIENT_SECRET, "Please supply your client_secret."
	data = urlencode({
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'grant_type': GRANT_TYPE,
	})
	headers = {
		'content-type': 'application/x-www-form-urlencoded',
	}
	response = requests.request('POST', url, data=data, headers=headers)
	bearer_token = response.json()['access_token']
	return bearer_token


def request(host, path, bearer_token, url_params=None):
	"""Given a bearer token, send a GET request to the API.
	Args:
		host (str): The domain host of the API.
		path (str): The path of the API after the domain.
		bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
		url_params (dict): An optional set of query parameters in the request.
	Returns:
		dict: The JSON response from the request.
	Raises:
		HTTPError: An error occurs from the HTTP request.
	"""
	url_params = url_params or {}
	url = '{0}{1}'.format(host, quote(path.encode('utf8')))
	headers = {
		'Authorization': 'Bearer %s' % bearer_token,
	}

	print(u'Querying {0} ...'.format(url))

	response = requests.request('GET', url, headers=headers, params=url_params)

	return response.json()


def search(bearer_token, term, location):
	"""Query the Search API by a search term and location.
	Args:
		term (str): The search term passed to the API.
		location (str): The search location passed to the API.
	Returns:
		dict: The JSON response from the request.
	"""

	url_params = {
		'term': term.replace(' ', '+'),
		'location': location.replace(' ', '+'),
		'limit': SEARCH_LIMIT
	}
	return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def get_business(bearer_token, business_id):
	"""Query the Business API by a business ID.
	Args:
		business_id (str): The ID of the business to query.
	Returns:
		dict: The JSON response from the request.
	"""
	business_path = BUSINESS_PATH + business_id

	return request(API_HOST, business_path, bearer_token)



"""
 Queries the API by the input values from the user.
	Args:
		term (str): The search term to query.
		location (str): The location of the business to query.
	 businesses = response.get('businesses')

	if not businesses:
	   print(u'No businesses for {0} in {1} found.'.format(term, location))
		return

	business_id = businesses[0]['id']

	print(u'{0} businesses found, querying business info ' \
		'for the top result "{1}" ...'.format(
			len(businesses), business_id))
	response = get_business(bearer_token, business_id)

	print(u'Result for business "{0}" found:'.format(business_id))
"""

def query_api(term, location,xyz):
   
	bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

	response = search(bearer_token, term, location)
	
	logFile=open('C:\\Users\\raosa\\AnacondaProjects\\indaroma-dataviz-pythoncode\\data\\'+DEFAULT_LOCATION[xyz]+'.json', 'w')
	pprint.pprint(response, logFile, indent=2)


def main():
	for xyz in range(0,1253):
		parser = argparse.ArgumentParser()

		parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
							type=str, help='Search term (default: %(default)s)')
		parser.add_argument('-l', '--location', dest='location',
							default=DEFAULT_LOCATION[xyz], type=str,
							help='Search location (default: %(default)s)')

		input_values = parser.parse_args()

		try:
			query_api(input_values.term, input_values.location,xyz)
			
		except HTTPError as error:
			sys.exit(
				'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
					error.code,
					error.url,
					error.read(),
						)
			)
	
	
if __name__ == '__main__':
	main()