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
DEFAULT_LOCATION ='93412 California','93420 California','93421 California','93422 California','93423 California','93424 California','93426 California','93427 California','93428 California','93429 California','93430 California','93432 California','93433 California','93434 California','93435 California','93436 California','93437 California','93438 California','93440 California','93441 California','93442 California','93443 California','93444 California','93445 California','93446 California','93447 California','93448 California','93449 California','93450 California','93451 California','93452 California','93453 California','93454 California','93455 California','93456 California','93457 California','93458 California','93460 California','93461 California','93463 California','93464 California','93465 California','93475 California','93483 California','93501 California','93502 California','93504 California','93505 California','93510 California','93512 California','93513 California','93514 California','93515 California','93516 California','93517 California','93518 California','93519 California','93522 California','93523 California','93524 California','93526 California','93527 California','93528 California','93529 California','93530 California','93531 California','93532 California','93534 California','93535 California','93536 California','93539 California','93541 California','93542 California','93543 California','93544 California','93545 California','93546 California','93549 California','93550 California','93551 California','93552 California','93553 California','93554 California','93555 California','93556 California','93558 California','93560 California','93561 California','93562 California','93563 California','93581 California','93584 California','93586 California','93590 California','93591 California','93592 California','93596 California','93599 California','93601 California','93602 California','93603 California','93604 California','93605 California','93606 California','93607 California','93608 California','93609 California','93610 California','93611 California','93612 California','93613 California','93614 California','93615 California','93616 California','93618 California','93619 California','93620 California','93621 California','93622 California','93623 California','93624 California','93625 California','93626 California','93627 California','93628 California','93630 California','93631 California','93633 California','93634 California','93635 California','93636 California','93637 California','93638 California','93639 California','93640 California','93641 California','93642 California','93643 California','93644 California','93645 California','93646 California','93647 California','93648 California','93649 California','93650 California','93651 California','93652 California','93653 California','93654 California','93656 California','93657 California','93660 California','93661 California','93662 California','93664 California','93665 California','93666 California','93667 California','93668 California','93669 California','93670 California','93673 California','93675 California','93701 California','93702 California','93703 California','93704 California','93705 California','93706 California','93707 California','93708 California','93709 California','93710 California','93711 California','93712 California','93714 California','93715 California','93716 California','93717 California','93718 California','93720 California','93721 California','93722 California','93723 California','93724 California','93725 California','93726 California','93727 California','93728 California','93729 California','93730 California','93737 California','93740 California','93741 California','93744 California','93745 California','93747 California','93750 California','93755 California','93760 California','93761 California','93764 California','93765 California','93771 California','93772 California','93773 California','93774 California','93775 California','93776 California','93777 California','93778 California','93779 California','93786 California','93790 California','93791 California','93792 California','93793 California','93794 California','93844 California','93888 California','93901 California','93902 California','93905 California','93906 California','93907 California','93908 California','93912 California','93915 California','93920 California','93921 California','93922 California','93923 California','93924 California','93925 California','93926 California','93927 California','93928 California','93930 California','93932 California','93933 California','93940 California','93942 California','93943 California','93944 California','93950 California','93953 California','93954 California','93955 California','93960 California','93962 California','94002 California','94005 California','94010 California','94011 California','94014 California','94015 California','94016 California','94017 California','94018 California','94019 California','94020 California','94021 California','94022 California','94023 California','94024 California','94025 California','94026 California','94027 California','94028 California','94030 California','94035 California','94037 California','94038 California','94039 California','94040 California','94041 California','94042 California','94043 California','94044 California','94060 California','94061 California','94062 California','94063 California','94064 California','94065 California','94066 California','94070 California','94074 California','94080 California','94083 California','94085 California','94086 California','94087 California','94088 California','94089 California','94102 California','94103 California','94104 California','94105 California','94107 California','94108 California','94109 California','94110 California','94111 California','94112 California','94114 California','94115 California','94116 California','94117 California','94118 California','94119 California','94120 California','94121 California','94122 California','94123 California','94124 California','94125 California','94126 California','94127 California','94128 California','94129 California','94130 California','94131 California','94132 California','94133 California','94134 California','94137 California','94139 California','94140 California','94141 California','94142 California','94143 California','94144 California','94145 California','94146 California','94147 California','94151 California','94158 California','94159 California','94160 California','94161 California','94163 California','94164 California','94172 California','94177 California','94188 California','94203 California','94204 California','94205 California','94206 California','94207 California','94208 California','94209 California','94211 California','94229 California','94230 California','94232 California','94234 California','94235 California','94236 California','94237 California','94239 California','94240 California','94244 California','94245 California','94247 California','94248 California','94249 California','94250 California','94252 California','94254 California','94256 California','94257 California','94258 California','94259 California','94261 California','94262 California','94263 California','94267 California','94268 California','94269 California','94271 California','94273 California','94274 California','94277 California','94278 California','94279 California','94280 California','94282 California','94283 California','94284 California','94285 California','94286 California','94287 California','94288 California','94289 California','94290 California','94291 California','94293 California','94294 California','94295 California','94296 California','94297 California','94298 California','94299 California','94301 California','94302 California','94303 California','94304 California','94305 California','94306 California','94309 California','94401 California','94402 California','94403 California','94404 California','94497 California','94501 California','94502 California','94503 California','94505 California','94506 California','94507 California','94508 California','94509 California','94510 California','94511 California','94512 California','94513 California','94514 California','94515 California','94516 California','94517 California','94518 California','94519 California','94520 California','94521 California','94522 California','94523 California','94524 California','94525 California','94526 California','94527 California','94528 California','94529 California','94530 California','94531 California','94533 California','94534 California','94535 California','94536 California','94537 California','94538 California','94539 California','94540 California','94541 California','94542 California','94543 California','94544 California','94545 California','94546 California','94547 California','94548 California','94549 California','94550 California','94551 California','94552 California','94553 California','94555 California','94556 California','94557 California','94558 California','94559 California','94560 California','94561 California','94562 California','94563 California','94564 California','94565 California','94566 California','94567 California','94568 California','94569 California','94570 California','94571 California','94572 California','94573 California','94574 California','94575 California','94576 California','94577 California','94578 California','94579 California','94580 California','94581 California','94582 California','94583 California','94585 California','94586 California','94587 California','94588 California','94589 California','94590 California','94591 California','94592 California','94595 California','94596 California','94597 California','94598 California','94599 California','94601 California','94602 California','94603 California','94604 California','94605 California','94606 California','94607 California','94608 California','94609 California','94610 California','94611 California','94612 California','94613 California','94614 California','94615 California','94617 California','94618 California','94619 California','94620 California','94621 California','94622 California','94623 California','94624 California','94649 California','94659 California','94660 California','94661 California','94662 California','94666 California','94701 California','94702 California','94703 California','94704 California','94705 California','94706 California','94707 California','94708 California','94709 California','94710 California','94712 California','94720 California','94801 California','94802 California','94803 California','94804 California','94805 California','94806 California','94807 California','94808 California','94820 California','94850 California','94901 California','94903 California','94904 California','94912 California','94913 California','94914 California','94915 California','94920 California','94922 California','94923 California','94924 California','94925 California','94926 California','94927 California','94928 California','94929 California','94930 California','94931 California','94933 California','94937 California','94938 California','94939 California','94940 California','94941 California','94942 California','94945 California','94946 California','94947 California','94948 California','94949 California','94950 California','94951 California','94952 California','94953 California','94954 California','94955 California','94956 California','94957 California','94960 California','94963 California','94964 California','94965 California','94966 California','94970 California','94971 California','94972 California','94973 California','94974 California','94975 California','94976 California','94977 California','94978 California','94979 California','94998 California','94999 California','95001 California','95002 California','95003 California','95004 California','95005 California','95006 California','95007 California','95008 California','95009 California','95010 California','95011 California','95012 California','95013 California','95014 California','95015 California','95017 California','95018 California','95019 California','95020 California','95021 California','95023 California','95024 California','95026 California','95030 California','95031 California','95032 California','95033 California','95035 California','95036 California','95037 California','95038 California','95039 California','95041 California','95042 California','95043 California','95044 California','95045 California','95046 California','95050 California','95051 California','95052 California','95053 California','95054 California','95055 California','95056 California','95060 California','95061 California','95062 California','95063 California','95064 California','95065 California','95066 California','95067 California','95070 California','95071 California','95073 California','95075 California','95076 California','95077 California','95101 California','95103 California','95106 California','95108 California','95109 California','95110 California','95111 California','95112 California','95113 California','95115 California','95116 California','95117 California','95118 California','95119 California','95120 California','95121 California','95122 California','95123 California','95124 California','95125 California','95126 California','95127 California','95128 California','95129 California','95130 California','95131 California','95132 California','95133 California','95134 California','95135 California','95136 California','95138 California','95139 California','95140 California','95141 California','95148 California','95150 California','95151 California','95152 California','95153 California','95154 California','95155 California','95156 California','95157 California','95158 California','95159 California','95160 California','95161 California','95164 California','95170 California','95172 California','95173 California','95190 California','95191 California','95192 California','95193 California','95194 California','95196 California','95201 California','95202 California','95203 California','95204 California','95205 California','95206 California','95207 California','95208 California','95209 California','95210 California','95211 California','95212 California','95213 California','95215 California','95219 California','95220 California','95221 California','95222 California','95223 California','95224 California','95225 California','95226 California','95227 California','95228 California','95229 California','95230 California','95231 California','95232 California','95233 California','95234 California','95236 California','95237 California','95240 California','95241 California','95242 California','95245 California','95246 California','95247 California','95248 California','95249 California','95251 California','95252 California','95253 California','95254 California','95255 California','95257 California','95258 California','95267 California','95269 California','95296 California','95297 California','95301 California','95303 California','95304 California','95305 California','95306 California','95307 California','95309 California','95310 California','95311 California','95312 California','95313 California','95315 California','95316 California','95317 California','95318 California','95319 California','95320 California','95321 California','95322 California','95323 California','95324 California','95325 California','95326 California','95327 California','95328 California','95329 California','95330 California','95333 California','95334 California','95335 California','95336 California','95337 California','95338 California','95340 California','95341 California','95343 California','95344 California','95345 California','95346 California','95347 California','95348 California','95350 California','95351 California','95352 California','95353 California','95354 California','95355 California','95356 California','95357 California','95358 California','95360 California','95361 California','95363 California','95364 California','95365 California','95366 California','95367 California','95368 California','95369 California','95370 California','95372 California','95373 California','95374 California','95375 California','95376 California','95377 California','95378 California','95379 California','95380 California','95381 California','95382 California','95383 California','95385 California','95386 California','95387 California','95388 California','95389 California','95391 California','95397 California','95401 California','95402 California','95403 California','95404 California','95405 California','95406 California','95407 California','95409 California','95410 California','95412 California','95415 California','95416 California','95417 California','95418 California','95419 California','95420 California','95421 California','95422 California','95423 California','95424 California','95425 California','95426 California','95427 California','95428 California','95429 California','95430 California','95431 California','95432 California','95433 California','95435 California','95436 California','95437 California','95439 California','95441 California','95442 California','95443 California','95444 California','95445 California','95446 California','95448 California','95449 California','95450 California','95451 California','95452 California','95453 California','95454 California','95456 California','95457 California','95458 California','95459 California','95460 California','95461 California','95462 California','95463 California','95464 California','95465 California','95466 California','95467 California','95468 California','95469 California','95470 California','95471 California','95472 California','95473 California','95476 California','95480 California','95481 California','95482 California','95485 California','95486 California','95487 California','95488 California','95490 California','95492 California','95493 California','95494 California','95497 California','95501 California','95502 California','95503 California','95511 California','95514 California','95518 California','95519 California','95521 California','95524 California','95525 California','95526 California','95527 California','95528 California','95531 California','95532 California','95534 California','95536 California','95537 California','95538 California','95540 California','95542 California','95543 California','95545 California','95546 California','95547 California','95548 California','95549 California','95550 California','95551 California','95552 California','95553 California','95554 California','95555 California','95556 California','95558 California','95559 California','95560 California','95562 California','95563 California','95564 California','95565 California','95567 California','95568 California','95569 California','95570 California','95571 California','95573 California','95585 California','95587 California','95589 California','95595 California','95601 California','95602 California','95603 California','95604 California','95605 California','95606 California','95607 California','95608 California','95609 California','95610 California','95611 California','95612 California','95613 California','95614 California','95615 California','95616 California','95617 California','95618 California','95619 California','95620 California','95621 California','95623 California','95624 California','95625 California','95626 California','95627 California','95628 California','95629 California','95630 California','95631 California','95632 California','95633 California','95634 California','95635 California','95636 California','95637 California','95638 California','95639 California','95640 California','95641 California','95642 California','95644 California','95645 California','95646 California','95648 California','95650 California','95651 California','95652 California','95653 California','95654 California','95655 California','95656 California','95658 California','95659 California','95660 California','95661 California','95662 California','95663 California','95664 California','95665 California','95666 California','95667 California','95668 California','95669 California','95670 California','95671 California','95672 California','95673 California','95674 California','95675 California','95676 California','95677 California','95678 California','95679 California','95680 California','95681 California','95682 California','95683 California','95684 California','95685 California','95686 California','95687 California','95688 California','95689 California','95690 California','95691 California','95692 California','95693 California','95694 California','95695 California','95696 California','95697 California','95698 California','95699 California','95701 California','95703 California','95709 California','95712 California','95713 California','95714 California','95715 California','95717 California','95720 California','95721 California','95722 California','95724 California','95726 California','95728 California','95735 California','95736 California','95741 California','95742 California','95746 California','95747 California','95757 California','95758 California','95759 California','95762 California','95763 California','95765 California','95776 California','95798 California','95799 California','95811 California','95812 California','95813 California','95814 California','95815 California','95816 California','95817 California','95818 California','95819 California','95820 California','95821 California','95822 California','95823 California','95824 California','95825 California','95826 California','95827 California','95828 California','95829 California','95830 California','95831 California','95832 California','95833 California','95834 California','95835 California','95836 California','95837 California','95838 California','95840 California','95841 California','95842 California','95843 California','95851 California','95852 California','95853 California','95860 California','95864 California','95865 California','95866 California','95867 California','95894 California','95899 California','95901 California','95903 California','95910 California','95912 California','95913 California','95914 California','95915 California','95916 California','95917 California','95918 California','95919 California','95920 California','95922 California','95923 California','95924 California','95925 California','95926 California','95927 California','95928 California','95929 California','95930 California','95932 California','95934 California','95935 California','95936 California','95937 California','95938 California','95939 California','95940 California','95941 California','95942 California','95943 California','95944 California','95945 California','95946 California','95947 California','95948 California','95949 California','95950 California','95951 California','95953 California','95954 California','95955 California','95956 California','95957 California','95958 California','95959 California','95960 California','95961 California','95962 California','95963 California','95965 California','95966 California','95967 California','95968 California','95969 California','95970 California','95971 California','95972 California','95973 California','95974 California','95975 California','95976 California','95977 California','95978 California','95979 California','95980 California','95981 California','95982 California','95983 California','95984 California','95986 California','95987 California','95988 California','95991 California','95992 California','95993 California','96001 California','96002 California','96003 California','96006 California','96007 California','96008 California','96009 California','96010 California','96011 California','96013 California','96014 California','96015 California','96016 California','96017 California','96019 California','96020 California','96021 California','96022 California','96023 California','96024 California','96025 California','96027 California','96028 California','96029 California','96031 California','96032 California','96033 California','96034 California','96035 California','96037 California','96038 California','96039 California','96040 California','96041 California','96044 California','96046 California','96047 California','96048 California','96049 California','96050 California','96051 California','96052 California','96054 California','96055 California','96056 California','96057 California','96058 California','96059 California','96061 California','96062 California','96063 California','96064 California','96065 California','96067 California','96068 California','96069 California','96070 California','96071 California','96073 California','96074 California','96075 California','96076 California','96078 California','96079 California','96080 California','96084 California','96085 California','96086 California','96087 California','96088 California','96089 California','96090 California','96091 California','96092 California','96093 California','96094 California','96095 California','96096 California','96097 California','96099 California','96101 California','96103 California','96104 California','96105 California','96106 California','96107 California','96108 California','96109 California','96110 California','96111 California','96112 California','96113 California','96114 California','96115 California','96116 California','96117 California','96118 California','96119 California','96120 California','96121 California','96122 California','96123 California','96124 California','96125 California','96126 California','96127 California','96128 California','96129 California','96130 California','96132 California','96133 California','96134 California','96135 California','96136 California','96137 California','96140 California','96141 California','96142 California','96143 California','96145 California','96146 California','96148 California','96150 California','96151 California','96152 California','96154 California','96155 California','96156 California','96157 California','96158 California','96160 California','96161 California','96162 California'
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

