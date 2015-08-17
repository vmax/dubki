#!/usr/bin/env python

from datetime import datetime,time
from datetime import timedelta

map_sources = {
	'aeroport' : '9kfYmO7lbg2o_YuSTvZqiY9rCevo23cs',
	'strogino' : 'pMeBRyKZjz3PnQn4HCZKIlagbMIv2Bxp',
	'tekstilshiki' : 'IcVLk9vNC1afHy5ge05Ae07wahHXZZ7H',
	'st_basmannaya' : 'LwunOFh66TXk8NyRAgKpsssV0Gdy34pG',
	'vavilova'  : '_Cz-NprpRRfD15AECXvyxGQb5N7RY3xC',
	'myasnitskaya'  : 'GGWd7qLfRklaR5KSQQpKFOiJT8RPFGO-',
	'izmailovo'  : 'tTSwzei04UwodpOe5ThQSKwo47ZiR8aO',
	'shabolovskaya'  : '0enMIqcJ_dLy8ShEHN34Lu-4XBAHsrno',
	'petrovka'  :  'pSiE6gI2ftRfAGBDauSW0G0H2o9R726u'
}

deltas = {
	'aeroport': timedelta(minutes=14),
	'strogino' : timedelta (minutes=6),
	'tekstilshiki' : timedelta (minutes=10),
	'st_basmannaya' : timedelta (minutes=16),
	'vavilova'  : timedelta (minutes=5),
	'myasnitskaya'  : timedelta (minutes=6),
	'izmailovo'  : timedelta (minutes=16),
	'shabolovskaya'  : timedelta (minutes=4),
	'petrovka'  : timedelta (minutes=6)
}

def form_map_url (edu, type='img'):
	if type=='img':
		return 'https://api-maps.yandex.ru/services/constructor/1.0/static/?sid=%s' % map_sources[edu]
	elif type=='script':
		return 'https://api-maps.yandex.ru/services/constructor/1.0/js/?sid=%s' % map_sources[edu]


# passing from subway to edu (or vice versa)
def get_nearest_onfoot (edu,_timestamp):
	result = dict()
	result['departure'] = _timestamp
	result['mapsrc'] = form_map_url(edu)
	result['time'] = deltas[edu]
	result['arrival'] = result['departure'] + result['time']
	return result