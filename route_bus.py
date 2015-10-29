#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        A module which calculates the nearest bus using an external API
        Running as a script calls `fetch_and_save_bus_schedule()`
        Note that this behaviour is likely to change in future
"""

import json
import urllib
from urllib import request
from datetime import datetime, timedelta

#: URL of bus schedule API provider
BUS_API_URL = "http://dubkiapi2.appspot.com/sch"
#: cached bus schedule filename
SCHEDULE_FILE = ".bus_schedule"


def fetch_and_save_bus_schedule():
    """
        Caches the bus schedule to `SCHEDULE_FILE`
    """
    schedule = urllib.request.urlopen(BUS_API_URL).read().decode()
    with open(SCHEDULE_FILE, 'w') as schedule_file:
        schedule_file.write(schedule)


def get_nearest_bus(_from, _to, _timestamp):
    """
        Returns the nearest bus

        Args:
            _from(str): place of departure
            _to(str): place of arrival
            _timestamp(datetime): time of departure

        Note:
            `_from` and `_to` should not be equal and should be in {'Одинцово', 'Дубки'}
    """
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

    with open(SCHEDULE_FILE) as schedule_file:
        schedule = json.loads(schedule_file.read())

    for elem in schedule:
        if elem['from'] == _from and elem['to'] == _to:
            current_schedule = elem

    times = [time['time'] for time in current_schedule['hset']]
    bustimes = []

    # get the nearest time
    delta = timedelta.max

    for time in times:
        sl_blvd_bus = False
        # asterisk indicates bus arrival // departure station is 'Славянский бульвар'
        # it needs special handling
        if '*' in time:
            sl_blvd_bus = True
        time = time.strip('*')
        bus_time = datetime.strptime(time, '%H:%M')
        bus_time = bus_time.replace(
            day=_timestamp.day,
            month=_timestamp.month,
            year=_timestamp.year)
        if bus_time < _timestamp:  # FIXME works incorrectly between weekday 6-7-1
            bus_time += timedelta(days=1)
        bustimes.append((bus_time, sl_blvd_bus))

    for time in bustimes:
        if time[0] - _timestamp < delta:
            delta = time[0] - _timestamp
            bus_time_res = time

    # fixing the parameter for pretty displaying
    # we like 'Дубки' better than 'ДубкиСуббота'
    _from = _from.replace('Суббота', '').replace('Воскресенье', '')
    _to = _to.replace('Суббота', '').replace('Воскресенье', '')

    delta = timedelta(minutes=15)
    # FIXME: more real arrival time?
    if bus_time_res[1] is True:  # blvd bus
        if _to == 'Одинцово':
            _to = 'Славянский бульвар'
        elif _from == 'Одинцово':
            _from = 'Славянский бульвар'
        delta = timedelta(minutes=50)

    return {'from': _from,
            'to': _to,
            'departure': bus_time_res[0],
            'arrival': bus_time_res[0] + delta}

# we run as a script
if __name__ == "__main__":
    fetch_and_save_bus_schedule()
