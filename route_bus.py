#!/usr/bin/env python

import urllib
import datetime
import json
from urllib import request
from datetime import datetime
from datetime import timedelta

BUS_API_URL = "http://dubkiapi2.appspot.com/sch"
SCHEDULE_FILE = ".bus_schedule"

def fetch_and_save_bus_schedule():
	schedule = urllib.request.urlopen(BUS_API_URL).read().decode()
	with open(SCHEDULE_FILE, 'w') as F:
		F.write(schedule)

# _from and _to should be in {'Одинцово', 'Дубки'}
def get_nearest_bus(_from,_to,_timestamp):
	assert _from in {'Одинцово', 'Дубки'}
	assert _to in {'Одинцово', 'Дубки'}
	assert _from != _to

	weekday = _timestamp.isoweekday()
	# today is either {'','*Суббота', '*Воскресенье'}
	if weekday == 6:
		if _from == 'Дубки':
			_from = 'ДубкиСуббота'
		elif _to == 'Дубки':
			_to = 'ДубкиСуббота'
	elif weekday == 7:
		if _from == 'Дубки':
			_from = 'ДубкиВоскресенье'
		elif _to == 'Дубки':
			_to = 'ДубкиВоскресенье'

	with open(SCHEDULE_FILE) as F:
		schedule = json.loads(F.read())

	for elem in schedule:
		if elem['from'] == _from and elem['to'] == _to:
			current_schedule = elem

	times = [time['time'] for time in current_schedule['hset']]
	
	# get the nearest time

	delta = timedelta.max

	for time in times:
		# FIXME: asterisk indicates bus arrival // departure station is 'Славянский бульвар'
		# it needs special handling
		time = time.strip('*')
		bus_time = datetime.strptime(time, '%H:%M')
		bus_time = bus_time.replace(day=_timestamp.day, month=_timestamp.month, year=_timestamp.year)
		if bus_time < _timestamp:
			bus_time += timedelta(days=1)
		newdelta = bus_time - _timestamp
		# looking for minimum delta between current time and bus departure time
		# and keeping in mind that bus should be in future
		# TODO: save more than one result
		if newdelta < delta:
			delta = newdelta
			bus_time_res = bus_time

	# fixing the parameter for pretty displaying
	# we like 'Дубки' better than 'ДубкиСуббота'
	_from = _from.replace('Суббота','').replace('Воскресенье','')
	_to = _to.replace('Суббота','').replace('Воскресенье','')
            
	# FIXME: more real arrival time?
	query_result = {'from' : _from, 'to' : _to, 'departure': bus_time_res, 'arrival': bus_time_res + timedelta(minutes=20)}
	return query_result

# we run as a script
if __name__ == "__main__":
	fetch_and_save_bus_schedule()