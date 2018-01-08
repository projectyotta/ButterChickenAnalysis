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
DEFAULT_LOCATION = '80001 Colorado','80002 Colorado','80003 Colorado','80004 Colorado','80005 Colorado','80006 Colorado','80007 Colorado','80010 Colorado','80011 Colorado','80012 Colorado','80013 Colorado','80014 Colorado','80015 Colorado','80016 Colorado','80017 Colorado','80018 Colorado','80019 Colorado','80020 Colorado','80021 Colorado','80022 Colorado','80023 Colorado','80024 Colorado','80025 Colorado','80026 Colorado','80027 Colorado','80030 Colorado','80031 Colorado','80033 Colorado','80034 Colorado','80035 Colorado','80036 Colorado','80037 Colorado','80038 Colorado','80040 Colorado','80041 Colorado','80042 Colorado','80044 Colorado','80045 Colorado','80046 Colorado','80047 Colorado','80101 Colorado','80102 Colorado','80103 Colorado','80104 Colorado','80105 Colorado','80106 Colorado','80107 Colorado','80108 Colorado','80109 Colorado','80110 Colorado','80111 Colorado','80112 Colorado','80113 Colorado','80116 Colorado','80117 Colorado','80118 Colorado','80120 Colorado','80121 Colorado','80122 Colorado','80123 Colorado','80124 Colorado','80125 Colorado','80126 Colorado','80127 Colorado','80128 Colorado','80129 Colorado','80130 Colorado','80131 Colorado','80132 Colorado','80133 Colorado','80134 Colorado','80135 Colorado','80136 Colorado','80137 Colorado','80138 Colorado','80150 Colorado','80151 Colorado','80155 Colorado','80160 Colorado','80161 Colorado','80162 Colorado','80163 Colorado','80165 Colorado','80166 Colorado','80201 Colorado','80202 Colorado','80203 Colorado','80204 Colorado','80205 Colorado','80206 Colorado','80207 Colorado','80208 Colorado','80209 Colorado','80210 Colorado','80211 Colorado','80212 Colorado','80214 Colorado','80215 Colorado','80216 Colorado','80217 Colorado','80218 Colorado','80219 Colorado','80220 Colorado','80221 Colorado','80222 Colorado','80223 Colorado','80224 Colorado','80225 Colorado','80226 Colorado','80227 Colorado','80228 Colorado','80229 Colorado','80230 Colorado','80231 Colorado','80232 Colorado','80233 Colorado','80234 Colorado','80235 Colorado','80236 Colorado','80237 Colorado','80238 Colorado','80239 Colorado','80241 Colorado','80243 Colorado','80244 Colorado','80246 Colorado','80247 Colorado','80248 Colorado','80249 Colorado','80250 Colorado','80251 Colorado','80252 Colorado','80256 Colorado','80257 Colorado','80259 Colorado','80260 Colorado','80261 Colorado','80262 Colorado','80263 Colorado','80264 Colorado','80265 Colorado','80266 Colorado','80271 Colorado','80273 Colorado','80274 Colorado','80281 Colorado','80290 Colorado','80291 Colorado','80293 Colorado','80294 Colorado','80299 Colorado','80301 Colorado','80302 Colorado','80303 Colorado','80304 Colorado','80305 Colorado','80306 Colorado','80307 Colorado','80308 Colorado','80309 Colorado','80310 Colorado','80314 Colorado','80401 Colorado','80402 Colorado','80403 Colorado','80419 Colorado','80420 Colorado','80421 Colorado','80422 Colorado','80423 Colorado','80424 Colorado','80425 Colorado','80426 Colorado','80427 Colorado','80428 Colorado','80429 Colorado','80430 Colorado','80432 Colorado','80433 Colorado','80434 Colorado','80435 Colorado','80436 Colorado','80437 Colorado','80438 Colorado','80439 Colorado','80440 Colorado','80442 Colorado','80443 Colorado','80444 Colorado','80446 Colorado','80447 Colorado','80448 Colorado','80449 Colorado','80451 Colorado','80452 Colorado','80453 Colorado','80454 Colorado','80455 Colorado','80456 Colorado','80457 Colorado','80459 Colorado','80461 Colorado','80463 Colorado','80465 Colorado','80466 Colorado','80467 Colorado','80468 Colorado','80469 Colorado','80470 Colorado','80471 Colorado','80473 Colorado','80474 Colorado','80475 Colorado','80476 Colorado','80477 Colorado','80478 Colorado','80479 Colorado','80480 Colorado','80481 Colorado','80482 Colorado','80483 Colorado','80487 Colorado','80488 Colorado','80497 Colorado','80498 Colorado','80501 Colorado','80502 Colorado','80503 Colorado','80504 Colorado','80510 Colorado','80511 Colorado','80512 Colorado','80513 Colorado','80514 Colorado','80515 Colorado','80516 Colorado','80517 Colorado','80520 Colorado','80521 Colorado','80522 Colorado','80523 Colorado','80524 Colorado','80525 Colorado','80526 Colorado','80527 Colorado','80528 Colorado','80530 Colorado','80532 Colorado','80533 Colorado','80534 Colorado','80535 Colorado','80536 Colorado','80537 Colorado','80538 Colorado','80539 Colorado','80540 Colorado','80541 Colorado','80542 Colorado','80543 Colorado','80544 Colorado','80545 Colorado','80546 Colorado','80547 Colorado','80549 Colorado','80550 Colorado','80551 Colorado','80553 Colorado','80601 Colorado','80602 Colorado','80603 Colorado','80610 Colorado','80611 Colorado','80612 Colorado','80614 Colorado','80615 Colorado','80620 Colorado','80621 Colorado','80622 Colorado','80623 Colorado','80624 Colorado','80631 Colorado','80632 Colorado','80633 Colorado','80634 Colorado','80638 Colorado','80639 Colorado','80640 Colorado','80642 Colorado','80643 Colorado','80644 Colorado','80645 Colorado','80646 Colorado','80648 Colorado','80649 Colorado','80650 Colorado','80651 Colorado','80652 Colorado','80653 Colorado','80654 Colorado','80701 Colorado','80705 Colorado','80720 Colorado','80721 Colorado','80722 Colorado','80723 Colorado','80726 Colorado','80727 Colorado','80728 Colorado','80729 Colorado','80731 Colorado','80732 Colorado','80733 Colorado','80734 Colorado','80735 Colorado','80736 Colorado','80737 Colorado','80740 Colorado','80741 Colorado','80742 Colorado','80743 Colorado','80744 Colorado','80745 Colorado','80746 Colorado','80747 Colorado','80749 Colorado','80750 Colorado','80751 Colorado','80754 Colorado','80755 Colorado','80757 Colorado','80758 Colorado','80759 Colorado','80801 Colorado','80802 Colorado','80804 Colorado','80805 Colorado','80807 Colorado','80808 Colorado','80809 Colorado','80810 Colorado','80812 Colorado','80813 Colorado','80814 Colorado','80815 Colorado','80816 Colorado','80817 Colorado','80818 Colorado','80819 Colorado','80820 Colorado','80821 Colorado','80822 Colorado','80823 Colorado','80824 Colorado','80825 Colorado','80826 Colorado','80827 Colorado','80828 Colorado','80829 Colorado','80830 Colorado','80831 Colorado','80832 Colorado','80833 Colorado','80834 Colorado','80835 Colorado','80836 Colorado','80840 Colorado','80841 Colorado','80860 Colorado','80861 Colorado','80862 Colorado','80863 Colorado','80864 Colorado','80866 Colorado','80901 Colorado','80902 Colorado','80903 Colorado','80904 Colorado','80905 Colorado','80906 Colorado','80907 Colorado','80908 Colorado','80909 Colorado','80910 Colorado','80911 Colorado','80912 Colorado','80913 Colorado','80914 Colorado','80915 Colorado','80916 Colorado','80917 Colorado','80918 Colorado','80919 Colorado','80920 Colorado','80921 Colorado','80922 Colorado','80923 Colorado','80924 Colorado','80925 Colorado','80926 Colorado','80927 Colorado','80928 Colorado','80929 Colorado','80930 Colorado','80931 Colorado','80932 Colorado','80933 Colorado','80934 Colorado','80935 Colorado','80936 Colorado','80937 Colorado','80938 Colorado','80939 Colorado','80941 Colorado','80942 Colorado','80944 Colorado','80946 Colorado','80947 Colorado','80949 Colorado','80950 Colorado','80951 Colorado','80960 Colorado','80962 Colorado','80970 Colorado','80977 Colorado','80995 Colorado','80997 Colorado','81001 Colorado','81002 Colorado','81003 Colorado','81004 Colorado','81005 Colorado','81006 Colorado','81007 Colorado','81008 Colorado','81009 Colorado','81010 Colorado','81011 Colorado','81012 Colorado','81019 Colorado','81020 Colorado','81021 Colorado','81022 Colorado','81023 Colorado','81024 Colorado','81025 Colorado','81027 Colorado','81029 Colorado','81030 Colorado','81033 Colorado','81034 Colorado','81036 Colorado','81038 Colorado','81039 Colorado','81040 Colorado','81041 Colorado','81043 Colorado','81044 Colorado','81045 Colorado','81046 Colorado','81047 Colorado','81049 Colorado','81050 Colorado','81052 Colorado','81054 Colorado','81055 Colorado','81057 Colorado','81058 Colorado','81059 Colorado','81062 Colorado','81063 Colorado','81064 Colorado','81067 Colorado','81069 Colorado','81071 Colorado','81073 Colorado','81076 Colorado','81077 Colorado','81081 Colorado','81082 Colorado','81084 Colorado','81087 Colorado','81089 Colorado','81090 Colorado','81091 Colorado','81092 Colorado','81101 Colorado','81102 Colorado','81120 Colorado','81121 Colorado','81122 Colorado','81123 Colorado','81124 Colorado','81125 Colorado','81126 Colorado','81128 Colorado','81129 Colorado','81130 Colorado','81131 Colorado','81132 Colorado','81133 Colorado','81135 Colorado','81136 Colorado','81137 Colorado','81138 Colorado','81140 Colorado','81141 Colorado','81143 Colorado','81144 Colorado','81146 Colorado','81147 Colorado','81148 Colorado','81149 Colorado','81151 Colorado','81152 Colorado','81154 Colorado','81155 Colorado','81157 Colorado','81201 Colorado','81210 Colorado','81211 Colorado','81212 Colorado','81215 Colorado','81220 Colorado','81221 Colorado','81222 Colorado','81223 Colorado','81224 Colorado','81225 Colorado','81226 Colorado','81227 Colorado','81228 Colorado','81230 Colorado','81231 Colorado','81232 Colorado','81233 Colorado','81235 Colorado','81236 Colorado','81237 Colorado','81239 Colorado','81240 Colorado','81241 Colorado','81242 Colorado','81243 Colorado','81244 Colorado','81248 Colorado','81251 Colorado','81252 Colorado','81253 Colorado','81290 Colorado','81301 Colorado','81302 Colorado','81303 Colorado','81320 Colorado','81321 Colorado','81323 Colorado','81324 Colorado','81325 Colorado','81326 Colorado','81327 Colorado','81328 Colorado','81329 Colorado','81330 Colorado','81331 Colorado','81332 Colorado','81334 Colorado','81335 Colorado','81401 Colorado','81402 Colorado','81403 Colorado','81410 Colorado','81411 Colorado','81413 Colorado','81414 Colorado','81415 Colorado','81416 Colorado','81418 Colorado','81419 Colorado','81420 Colorado','81422 Colorado','81423 Colorado','81424 Colorado','81425 Colorado','81426 Colorado','81427 Colorado','81428 Colorado','81429 Colorado','81430 Colorado','81431 Colorado','81432 Colorado','81433 Colorado','81434 Colorado','81435 Colorado','81501 Colorado','81502 Colorado','81503 Colorado','81504 Colorado','81505 Colorado','81506 Colorado','81507 Colorado','81520 Colorado','81521 Colorado','81522 Colorado','81523 Colorado','81524 Colorado','81525 Colorado','81526 Colorado','81527 Colorado','81601 Colorado','81602 Colorado','81610 Colorado','81611 Colorado','81612 Colorado','81615 Colorado','81620 Colorado','81621 Colorado','81623 Colorado','81624 Colorado','81625 Colorado','81626 Colorado','81630 Colorado','81631 Colorado','81632 Colorado','81633 Colorado','81635 Colorado','81636 Colorado','81637 Colorado','81638 Colorado','81639 Colorado','81640 Colorado','81641 Colorado','81642 Colorado','81643 Colorado','81645 Colorado','81646 Colorado','81647 Colorado','81648 Colorado','81649 Colorado','81650 Colorado','81652 Colorado','81653 Colorado','81654 Colorado','81655 Colorado','81656 Colorado','81657 Colorado','81658 Colorado'
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
	for xyz in range(0,2590):
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

