#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module which calculates the subway time
    It considers that the subway is closed from 1:00 AM till 5:50 AM
"""

from datetime import time, timedelta

#: precomputed times for subway trains
SUBWAY_DATA = {
    'Кунцевская': {
        'Строгино': timedelta(minutes=15),
        'Семёновская': timedelta(minutes=28),
        'Курская': timedelta(minutes=21),
        'Ленинский проспект': timedelta(minutes=28)},
    'Белорусская': {
        'Аэропорт': timedelta(minutes=6),
        'Тверская': timedelta(minutes=4)},
    'Беговая': {
        'Текстильщики': timedelta(minutes=22),
        'Лубянка': timedelta(minutes=12),
        'Шаболовская': timedelta(minutes=20),
        'Кузнецкий мост': timedelta(minutes=9),
        'Павелецкая': timedelta(minutes=17),
        'Китай-город': timedelta(minutes=11),
        'Третьяковская': timedelta(minutes=15)},
    'Славянский бульвар': {
        'Строгино':  timedelta(minutes=18),
        'Семёновская': timedelta(minutes=25),
        'Курская': timedelta(minutes=18),
        'Ленинский проспект': timedelta(minutes=25),
        'Аэропорт': timedelta(minutes=26),
        'Текстильщики': timedelta(minutes=35),
        'Лубянка': timedelta(minutes=21),
        'Шаболовская': timedelta(minutes=22),
        'Кузнецкий мост': timedelta(minutes=22),
        'Тверская': timedelta(minutes=22),
        'Китай-город': timedelta(minutes=25),
        'Третьяковская': timedelta(minutes=23)}
}


def subway_data_get(_from, _to):
    """
        Returns the time required to get from one subway station to another

        Args:
            _from(str): Russian name of station of departure
            _to(str): Russian name of station of arrival

        Note:
            `_from` and `_to` must exist in SUBWAY_DATA.keys or any of SUBWAY_DATA[key].values
    """
    return SUBWAY_DATA.get(_from, {}).get(_to) or SUBWAY_DATA.get(_to, {}).get(_from)

SUBWAY_CLOSES = time(hour=1)
SUBWAY_OPENS = time(hour=5, minute=50)


def get_nearest_subway(_from, _to, _timestamp):
    """
        Returns the nearest subway route

        Args:
            _from(str): Russian name of station of departure
            _to(str): Russian name of station of arrival
            _timestamp(datetime): time of departure

        Note:
            `_from` and `_to` must exist in SUBWAY_DATA.keys or any of SUBWAY_DATA[key].values
    """
    result = dict()
    if SUBWAY_CLOSES <= _timestamp.time() <= SUBWAY_OPENS:  # subway is still closed
        _timestamp.replace(
            hour=SUBWAY_OPENS.hour,
            minute=SUBWAY_OPENS.minute)
    result['departure'] = _timestamp
    result['arrival'] = result['departure'] + subway_data_get(_from, _to)
    result['from'] = _from
    result['to'] = _to
    return result
