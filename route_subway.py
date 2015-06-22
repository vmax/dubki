#!/usr/bin/env python

import json
from datetime import datetime,time
from datetime import timedelta

subway_data = {
	'Кунцевская': {
		'Строгино':  timedelta(minutes=15),
		'Семёновская': timedelta(minutes=28),
		'Курская': timedelta(minutes=21),
        		'Ленинский проспект' : timedelta(minutes=28)
	},
	'Белорусская': {
		'Аэропорт': timedelta(minutes=6)
	},
   	'Беговая' : {
        		'Текстильщики' : timedelta(minutes=22),
        		'Лубянка' : timedelta(minutes=12),
        		'Шаболовская' : timedelta(minutes=20),
        		'Кузнецкий мост': timedelta(minutes=9)

    	},
    	'Славянский бульвар': {
    		'Строгино':  timedelta(minutes=18),
		'Семёновская': timedelta(minutes=25),
		'Курская': timedelta(minutes=18),
        		'Ленинский проспект' : timedelta(minutes=25),
        		'Аэропорт': timedelta(minutes=26),
        		'Текстильщики' : timedelta(minutes=35),
        		'Лубянка' : timedelta(minutes=21),
        		'Шаболовская' : timedelta(minutes=22),
        		'Кузнецкий мост': timedelta(minutes=22)
    	}
}

subway_data_get = lambda _from, _to : subway_data.get(_from, {}).get(_to) or subway_data.get(_to, {}).get(_from)

subway_closes = time(hour=1)
subway_opens = time(hour=5, minute=50)

def get_nearest_subway(_from, _to, _timestamp):
	result = dict()
	if subway_closes <= _timestamp.time() <= subway_opens: # subway is still closed
		_timestamp.replace(hour=subway_opens.hour, minute=subway_opens.minute)
	result['departure'] = _timestamp
	result['arrival'] = result['departure'] + subway_data_get(_from,_to)
	result['from'] = _from
	result['to'] = _to
	return result