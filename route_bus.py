#!/usr/bin/env python

import urllib
import datetime
import json
from urllib import request
from datetime import datetime


BUS_API_URL = "http://dubkiapi2.appspot.com/sch"
SCHEDULE_FILE = ".bus_schedule"

def fetch_and_save_bus_schedule():
	schedule = urllib.request.urlopen(BUS_API_URL).read().decode()
	with open(SCHEDULE_FILE, 'w') as F:
		F.write(schedule)

# _from and _to should be in {'Одинцово', 'Дубки'}
def get_nearest_bus(_from,_to):
	assert _from in {'Одинцово', 'Дубки'}
	assert _to in {'Одинцово', 'Дубки'}
	assert _from != _to

	now = datetime.now()
	weekday = now.isoweekday()
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
			nearest_buses = elem

	print(nearest_buses)


# we run as a script
if __name__ == "__main__":
	fetch_and_save_bus_schedule()