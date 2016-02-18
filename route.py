#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module providing functionality for calculating routes
"""

from datetime import datetime
from datetime import timedelta
from route_bus import get_nearest_bus
from route_train import get_nearest_train
from route_subway import get_nearest_subway
from route_onfoot import get_nearest_onfoot
from logger import make_logger

ROUTE_LOG = make_logger('routing.log')
JSON_LOG = make_logger('json.log')
REVERSE_ROUTE_LOG = make_logger('reverse_routing.log')

#: list of dormitories
DORMS = {
    'dubki': 'Дубки',
    'odintsovo': 'Одинцово'
}

#: list of education campuses
EDUS = {
    'aeroport': 'Кочновский проезд (метро Аэропорт)',
    'strogino': 'Строгино',
    'myasnitskaya': 'Мясницкая (метро Лубянка)',
    'vavilova': 'Вавилова (метро Ленинский проспект)',
    'izmailovo': 'Кирпичная улица (метро Семёновская)',
    'tekstilshiki': 'Текстильщики',
    'st_basmannaya': 'Старая Басманная',
    'shabolovskaya': 'Шаболовская',
    'petrovka': 'Петровка (метро Кузнецкий мост)',
    'paveletskaya': 'Малая Пионерская (метро Павелецкая)',
    'ilyinka': 'Ильинка (метро Китай-город)',
    'trehsvyat_b': 'Большой Трёхсвятительский переулок (метро Китай-город)',
    'trehsvyat_m': 'Малый Трёхсвятительский переулок (метро Китай-город)',
    'hitra': 'Хитровский переулок (метро Китай-город)',
    'gnezdo': "Малый Гнездниковский переулок (метро Тверская)"
}

#: maps education campuses to preferred railway stations
PREF_STATIONS = {
    'aeroport': 'Белорусская',
    'strogino': 'Кунцево',
    'tekstilshiki': 'Беговая',
    'st_basmannaya': 'Кунцево',
    'vavilova': 'Кунцево',
    'myasnitskaya': 'Беговая',
    'izmailovo': 'Кунцево',
    'shabolovskaya': 'Беговая',
    'petrovka': 'Беговая',
    'paveletskaya': 'Беговая',
    'ilyinka': 'Беговая',
    'trehsvyat_b': 'Беговая',
    'trehsvyat_m': 'Беговая',
    'hitra': 'Беговая',
    'gnezdo': 'Белорусская'}

#: delta to pass from railway station to subway station
TTS_DELTAS = {
    'Кунцево': timedelta(minutes=10),
    'Фили': timedelta(minutes=7),
    'Беговая': timedelta(minutes=5),
    'Белорусская': timedelta(minutes=5)}

#: maps railway station names to subway station names
TTS_NAMES = {
    "Кунцево": "Кунцевская",
    "Фили": "Фили",
    "Беговая": "Беговая",
    "Белорусская": "Белорусская"}

#: maps education campuses to preferred subway stationsq
SUBWAYS = {
    'aeroport': 'Аэропорт',
    'myasnitskaya': 'Лубянка',
    'strogino': 'Строгино',
    'st_basmannaya':  'Курская',
    'tekstilshiki': 'Текстильщики',
    'vavilova': 'Ленинский проспект',
    'izmailovo': 'Семёновская',
    'shabolovskaya': 'Шаболовская',
    'petrovka': 'Кузнецкий мост',
    'paveletskaya': 'Павелецкая',
    'ilyinka': 'Китай-город',
    'trehsvyat_b': 'Китай-город',
    'trehsvyat_m': 'Китай-город',
    'hitra': 'Китай-город',
    'gnezdo': 'Тверская'}


def calculate_route_reverse(_from, _to, _timestamp_end):
    """
        Calculates a route as if timestamp is the time of arrival

        Args:
            _from (str): place of departure
            _to (str): place of arrival
            _timestamp_end(datetime): expected time of arrival

        Returns:
            route (dict): a calculated route
    """
    REVERSE_ROUTE_LOG("{_from} {_to} {_date}".format(
        _from=_from,
        _to=_to,
        _date=_timestamp_end.strftime('%d.%m.%Y %H:%M:%S')))
    departure_time = _timestamp_end - timedelta(hours=3, minutes=0)

    while True:
        route = calculate_route(_from, _to, departure_time, 'REVERSE')
        delta = _timestamp_end - route['arrival']
        if delta < timedelta(minutes=15):
            break
        else:
            departure_time += timedelta(minutes=5)

    return route


def calculate_route(_from, _to, _timestamp=datetime.now() + timedelta(minutes=10), src=None):
    """
        Calculates a route as if timestamp is the time of departure

        Args:
            _from (str): place of departure
            _to (str): place of arrival
            _timestamp(Optional[datetime]): time of departure.
                Defaults to the current time plus 10 minutes.
            src(Optional[str]): function caller ID (used for logging)

        Returns:
            route (dict): a calculated route
    """
    if src is None:  # function got called directly
        ROUTE_LOG("{_from} {_to}".format(
            _from=_from,
            _to=_to))
    elif src == 'JSON':  # called from JSON API
        JSON_LOG("{_from} {_to}".format(
            _from=_from,
            _to=_to))
    result = dict()
    result['_from'], result['_to'] = _from, _to
    departure = _timestamp
    if _from in DORMS:
        result['departure_place'] = 'dorm'
        result['departure'] = departure

        if _from == 'dubki':
            bus = get_nearest_bus('Дубки', 'Одинцово', result['departure'])
            result['bus'] = bus

            if bus['to'] == 'Славянский бульвар':  # blvd bus, we don't need train
                subway = get_nearest_subway(
                    'Славянский бульвар',
                    SUBWAYS[_to],
                    bus['arrival'] + timedelta(minutes=5))

                onfoot = get_nearest_onfoot(_to, subway['arrival'])
                result['train'] = None
                result['subway'] = subway
                result['onfoot'] = onfoot
                result['full_route_time'] = onfoot['arrival'] - bus['departure']
                result['arrival'] = onfoot['arrival']
                return result

        # adding 5 minutes to pass from bus to train
        train = get_nearest_train(
            'Одинцово',
            PREF_STATIONS[_to],
            (_from == 'dubki' and bus['arrival'] or departure) + timedelta(minutes=5))
        result['train'] = train

        subway = get_nearest_subway(
            TTS_NAMES[PREF_STATIONS[_to]],
            SUBWAYS[_to],
            train['arrival'] + TTS_DELTAS[PREF_STATIONS[_to]])

        result['subway'] = subway

        onfoot = get_nearest_onfoot(_to, subway['arrival'])
        result['onfoot'] = onfoot

        if _from == 'dubki':
            result['full_route_time'] = onfoot['arrival'] - bus['departure']
        else:
            result['full_route_time'] = onfoot['arrival'] - train['departure']

        result['arrival'] = onfoot['arrival']

    if _from in EDUS:
        result['departure_place'] = 'edu'
        result['departure'] = departure

        onfoot = get_nearest_onfoot(_from, departure)
        result['onfoot'] = onfoot

        subway = get_nearest_subway(
            SUBWAYS[_from],
            TTS_NAMES[PREF_STATIONS[_from]],
            onfoot['arrival'])
        result['subway'] = subway

        # TODO: add blvd buses
        train = get_nearest_train(
            PREF_STATIONS[_from],
            'Одинцово',
            subway['arrival'] + TTS_DELTAS[PREF_STATIONS[_from]])
        result['train'] = train

        if _to == 'dubki':
            bus = get_nearest_bus('Одинцово', 'Дубки', train['arrival'] + timedelta(minutes=5))
            result['bus'] = bus
            result['full_route_time'] = bus['arrival'] - onfoot['departure']
            result['arrival'] = bus['arrival']
        elif _to == 'odintsovo':
            result['full_route_time'] = train['arrival'] - onfoot['departure']
            result['arrival'] = train['arrival']

    # dirty-fix the result a bit
    if result.get('bus', None) and result['departure_place'] == 'dorm' and result['bus']['departure'] - result['departure'] > timedelta(minutes=10):
        result['departure'] = result['bus']['departure'] - timedelta(minutes=10)
    if not result.get('bus', None) and result['departure_place'] == 'dorm' and result['train']['departure'] - result['departure'] > timedelta(minutes=10):
        result['departure'] = result['train']['departure'] - timedelta(minutes=10)

    return result
