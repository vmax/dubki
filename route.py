#!/usr/bin/env python

from datetime import datetime
from route_bus import get_nearest_bus
from route_train import get_nearest_train

dorms = {
    'dubki' : 'Дубки',
}

edus = {
    'aeroport' : 'Кочна',
    'strogino' : 'Строгино',
    'myasnitskaya' : 'Мясо',
    'vavilova' : 'Вавилова',
    'izmailovo' : 'Кирпич',
    'tekstilshiki' : 'Текстильщики'
}

def calculate_route(_from, _to):
	result = dict()
	departure = datetime.now()
	# from dorm to edu, we start by bus
	# FIXME: add Odintsovo
	if _from in dorms:
		result['departure_place'] = 'dorm'
		result['departure'] = datetime.now()
		
		bus = get_nearest_bus('Дубки', 'Одинцово',departure)
		result['bus'] = bus

		train = get_nearest_train('Одинцово', 'Беговая', bus['arrival'])
		result['train'] =
	else:
		pass

	return result