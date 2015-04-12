#!/usr/bin/env python

import urllib
import json
from datetime import datetime
from urllib import request

API_KEY_FILE = ".train_api_key"

TRAIN_API_URL = """https://api.rasp.yandex.net/v1.0/search/?apikey=%s&format=json&date=%s&from=%s&to=%s&lang=ru&transport_types=suburban"""

STATIONS = {
	"Одинцово" : "c10743",
	"Кунцево": "s9752120",
	"Фили": "s9600821",
	"Беговая": "s9601666",
	"Белорусская": "s2000006"
}

def form_api_url(_from,_to):
	return TRAIN_API_URL % (get_key(),get_date(),STATIONS[_from],STATIONS[_to])

def get_key():
	with open(API_KEY_FILE) as F:
		key = F.read()
	return key

def get_nearest_train(_from, _to):
	assert _from in STATIONS
	assert _to in STATIONS

	now = datetime.now()

	schedule = json.loads(urllib.request.urlopen(form_api_url(_from, _to)).read().decode())

	print (schedule)


def get_date():
	return datetime.now().strftime('%Y-%m-%d')

# we run as a script
if __name__ == "__main__":
	fetch_and_save_bus_schedule()
