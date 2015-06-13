#!/usr/bin/env python

import urllib
import json
from datetime import datetime
from datetime import timedelta
from urllib import request

API_KEY_FILE = ".train_api_key"

TRAIN_API_URL = """https://api.rasp.yandex.net/v1.0/search/?apikey=%s&format=json&date=%s&from=%s&to=%s&lang=ru&transport_types=suburban"""

STATIONS = {
	"Одинцово" : "c10743",
	"Кунцево": "s9601728",
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

def get_nearest_train(_from, _to, _timestamp):
	assert _from in STATIONS
	assert _to in STATIONS

	schedule = json.loads(urllib.request.urlopen(form_api_url(_from, _to)).read().decode())
	#schedule =  json.loads(open('train_response_sample.json').read())

	trains = list()
	for train in schedule['threads']:
		_train = dict()
		_train['arrival'] = datetime.strptime(train['arrival'],'%Y-%m-%d %H:%M:%S')
		_train['departure'] = datetime.strptime(train['departure'],'%Y-%m-%d %H:%M:%S')
		_train['stops'] = train['stops']
		_train['to'] = _to
		_train['title'] = train['thread']['title']
		trains.append(_train)

	needed_train = None
	for train in trains:
		newdelta = train['departure'] - _timestamp
		if newdelta.days != -1:
			needed_train = train
			break
		else:
			delta = newdelta

	return needed_train

def get_date():
	return datetime.now().strftime('%Y-%m-%d')

# we run as a script
if __name__ == "__main__":
	fetch_and_save_bus_schedule()
