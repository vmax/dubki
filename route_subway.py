#!/usr/bin/env python

import json
from datetime import datetime
from datetime import timedelta

subway_data = {
	'Кунцевская': {
		'Строгино':  timedelta(minutes=15),
		'Семёновская': timedelta(minutes=28),
		'Курская': timedelta(minutes=21)
	},
	'Белорусская': {
		'Аэропорт': timedelta(minutes=6)
	}
}


def get_nearest_subway(_from, _to, _timestamp):
	result = dict()
	result['departure'] = _timestamp
	result['arrival'] = result['departure'] + subway_data[_from][_to]
	result['from'] = _from
	result['to'] = _to
	return result