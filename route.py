#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from route_bus import get_nearest_bus
from route_train import get_nearest_train
from route_subway import get_nearest_subway

dorms = {
    'dubki' : 'Дубки',
}

edus = {
    'aeroport' : 'Кочна',
    'strogino' : 'Строгино',
    'myasnitskaya' : 'Мясо',
    'vavilova' : 'Вавилова',
    'izmailovo' : 'Кирпич',
    'tekstilshiki' : 'Текстильщики',
    'st_basmannaya' : 'Старая Басманная'
}

# maps edus to preferred stations
pref_stations = {
	'aeroport': 'Белорусская',
	'strogino': 'Кунцево',
	'tekstilshiki': 'Беговая',
	 'st_basmannaya': 'Кунцево'
}

# delta to pass from railway station to subway station
tts_deltas = {
	'Кунцево': timedelta(minutes=10),
	'Фили': timedelta(minutes=7),
	'Беговая': timedelta(minutes=5),
	'Белорусская': timedelta(minutes=5)
}

tts_names = {
	"Кунцево": "Кунцевская",
	"Фили": "Фили",
	"Беговая": "Беговая",
	"Белорусская": "Белорусская"
}

subways = {
	'aeroport': 'Аэропорт',
	'myasnitskaya': 'Лубянка',
	'izmailovo':  'Семеновская',
	'strogino': 'Строгино',
	'st_basmannaya':  'Курская'
}

def calculate_route(_from, _to):
	result = dict()
	departure = datetime.now()
	# from dorm to edu, we start by bus
	# FIXME: add Odintsovo
	if _from in dorms:
		result['departure_place'] = 'dorm'
		result['departure'] = datetime.now()
		
		bus = get_nearest_bus('Дубки', 'Одинцово',result['departure'])
		result['bus'] = bus

		# adding 5 minutes to pass from bus to train
		train = get_nearest_train('Одинцово', pref_stations[_to], bus['arrival'] + timedelta(minutes=5))
		result['train'] = train

		print(train)

		subway = get_nearest_subway(
			tts_names[pref_stations[_to]],
			subways[_to],
			train['arrival'] + tts_deltas[pref_stations[_to]])

		result['subway'] = subway

	else:
		pass

	return result
