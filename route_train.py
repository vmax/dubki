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

def form_api_url(_from,_to,_timestamp):
	return TRAIN_API_URL % (get_key(),_timestamp.strftime('%Y-%m-%d'),STATIONS[_from],STATIONS[_to])

def get_key():
	with open(API_KEY_FILE) as F:
		key = F.read()
	return key.strip()

def cache_everything():
	from itertools import product as P
	for (_from,_to) in P(["Одинцово"], ["Кунцево","Фили","Беговая","Белорусская"]):
		cache_schedule(_from,_to,datetime.now())
		cache_schedule(_to,_from,datetime.now())

def cache_schedule(_from, _to,_timestamp):
	schedule_today = json.loads(urllib.request.urlopen(form_api_url(_from, _to,_timestamp)).read().decode())
	schedule_tomorrow = json.loads(urllib.request.urlopen(form_api_url(_from, _to,_timestamp+timedelta(days=1))).read().decode())
	schedule_tomorrow2 = json.loads(urllib.request.urlopen(form_api_url(_from, _to,_timestamp+timedelta(days=2))).read().decode())


	schedule = schedule_today['threads'] + schedule_tomorrow['threads'] + schedule_tomorrow2['threads']

	with open('train_cached_%s_%s' % (STATIONS[_from], STATIONS[_to]),'w') as F:
		json.dump(schedule, F)

def get_schedule (_from, _to,_timestamp):
	try:
		F = open('train_cached_%s_%s' % (STATIONS[_from], STATIONS[_to]))
		return json.load(F)
	except FileNotFoundError:
		cache_schedule(_from,_to, _timestamp)
		return get_schedule(_from,_to, _timestamp)


def get_nearest_train(_from, _to, _timestamp):
	assert _from in STATIONS
	assert _to in STATIONS

	schedule = get_schedule(_from,_to,_timestamp)

	trains = list()
	for train in schedule:
		_train = dict()
		_train['arrival'] = datetime.strptime(train['arrival'],'%Y-%m-%d %H:%M:%S')
		_train['departure'] = datetime.strptime(train['departure'],'%Y-%m-%d %H:%M:%S')
		_train['stops'] = train['stops']
		_train['to'] = _to
		_train['title'] = train['thread']['title']
		if _train['departure'] >= _timestamp:
			trains.append(_train)

	delta = timedelta.max

	for train in trains:
		newdelta = train['departure'] - _timestamp
		if newdelta < delta:
			needed_train = train
			delta = newdelta

	return needed_train

# we run as a script
if __name__ == "__main__":
	fetch_and_save_bus_schedule()
