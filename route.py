#!/usr/bin/env python

from datetime import datetime
from datetime import timedelta
from route_bus import get_nearest_bus
from route_train import get_nearest_train
from route_subway import get_nearest_subway
from route_onfoot import get_nearest_onfoot

dorms = {
    'dubki' : 'Дубки',
}

edus = {
    'aeroport' : 'Кочновский проезд (метро Аэропорт)',
    'strogino' : 'Строгино',
    'myasnitskaya' : 'Мясницкая (метро Лубянка)',
    'vavilova' : 'Вавилова (метро Ленинский проспект)',
    'izmailovo' : 'Кирпичная улица (метро Семёновская)',
    'tekstilshiki' : 'Текстильщики',
    'st_basmannaya' : 'Старая Басманная',
    'shabolovskaya' : 'Шаболовская',
    'petrovka' : 'Петровка (метро Кузнецкий мост)',
    'paveletskaya':'Малая Пионерская (метро Павелецкая)',
    'ilyinka': 'Ильинка (метро Китай-город)',
    'trehsvyat_b': 'Большой Трёхсвятительский переулок (метро Китай-город)',
    'trehsvyat_m': 'Малый Трёхсвятительский переулок (метро Китай-город)',
    'hitra': 'Хитровский переулок (метро Китай-город)'
}

# maps edus to preferred stations
pref_stations = {
	'aeroport': 'Белорусская',
	'strogino': 'Кунцево',
	'tekstilshiki': 'Беговая',
	'st_basmannaya': 'Кунцево',
	'vavilova' : 'Кунцево',
	'myasnitskaya' : 'Беговая',
	'izmailovo' : 'Кунцево',
	'shabolovskaya' : 'Беговая',
	'petrovka' : 'Беговая',
	'paveletskaya':'Беговая',
	'ilyinka': 'Беговая',
	'trehsvyat_b' : 'Беговая',
	'trehsvyat_m' : 'Беговая',
	'hitra' : 'Беговая'
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
	'strogino': 'Строгино',
	'st_basmannaya':  'Курская',
	'tekstilshiki': 'Текстильщики',
	'vavilova' : 'Ленинский проспект',
	'izmailovo' : 'Семёновская',
	'shabolovskaya' : 'Шаболовская',
	'petrovka' : 'Кузнецкий мост',
	'paveletskaya': 'Павелецкая',
	'ilyinka' : 'Китай-город',
	'trehsvyat_b' : 'Китай-город',
	'trehsvyat_m' : 'Китай-город',
	'hitra': 'Китай-город'
}

"""
	Calculates a route as if _timestamp is the time of arrival
"""
def calculate_route_reverse(_from,_to,_timestamp_end):
	departure_time = _timestamp_end - timedelta(hours=2,minutes=30)
	route = calculate_route(_from, _to, departure_time)
	delta = _timestamp_end - route['arrival']


	while route['departure'] >= datetime.now() and delta > timedelta(minutes=15):
		departure_time += timedelta(minutes=5)
		route = calculate_route(_from, _to, departure_time)
		delta = _timestamp_end - route['arrival']
	return route


def calculate_route(_from, _to, _timestamp = datetime.now() + timedelta(minutes=10)):
	result = dict()
	departure = _timestamp
	if _from in dorms:
		result['departure_place'] = 'dorm'
		result['departure'] = departure

		bus = get_nearest_bus('Дубки', 'Одинцово',result['departure'])
		result['bus'] = bus

		if bus['to'] == 'Славянский бульвар': # blvd bus, we don't need train
			subway = get_nearest_subway('Славянский бульвар',  subways[_to], bus['arrival'] + timedelta(minutes = 5))
			onfoot = get_nearest_onfoot(_to,subway['arrival'])
			result['train'] = None
			result['subway'] = subway
			result['onfoot'] = onfoot
			result['full_route_time'] = onfoot['arrival'] - bus['departure']
			result['arrival'] = onfoot['arrival']
			return result

		# adding 5 minutes to pass from bus to train
		train = get_nearest_train('Одинцово', pref_stations[_to], bus['arrival'] + timedelta(minutes=5))
		result['train'] = train

		subway = get_nearest_subway(
			tts_names[pref_stations[_to]],
			subways[_to],
			train['arrival'] + tts_deltas[pref_stations[_to]])

		result['subway'] = subway

		onfoot = get_nearest_onfoot (_to,subway['arrival'])
		result['onfoot'] = onfoot

		result['full_route_time'] = onfoot['arrival'] - bus['departure']
		result['arrival'] = onfoot['arrival']

	if _from in edus:
		result['departure_place'] = 'edu'
		result['departure'] = departure

		onfoot = get_nearest_onfoot(_from,departure)
		result['onfoot'] = onfoot

		subway = get_nearest_subway( subways[_from], tts_names[pref_stations[_from]], onfoot['arrival'])
		result['subway'] = subway

		# TODO: add blvd buses

		train = get_nearest_train(pref_stations[_from], 'Одинцово', subway['arrival'] + tts_deltas[pref_stations[_from]])
		result['train'] = train

		bus = get_nearest_bus('Одинцово', 'Дубки', train['arrival'] + timedelta(minutes=5))
		result['bus'] = bus

		result['full_route_time'] = bus['arrival'] - onfoot['departure']
		result['arrival'] = bus['arrival']

	return result
