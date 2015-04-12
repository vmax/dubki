#!/usr/bin/env python

import urllib
from datetime import datetime

API_KEY_FILE = ".train_api_key"

TRAIN_API_URL = """
https://api.rasp.yandex.net/v1.0/search/?apikey=%s 
&format=json
&date=%s
&from=%s
&to=%s
&lang=ru
&transport_types=suburban
"""

def form_api_url(_from,_to):
	return TRAIN_API_URL % (get_key(),get_date(),_from,_to)

def get_key():
	with open(API_KEY_FILE) as F:
		key = F.read()
	return key

def get_date():
	return datetime.now().strftime('%Y-%m-%d')
