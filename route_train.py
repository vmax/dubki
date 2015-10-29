#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        A module which calculates the nearest train using an external API (Yandex.Rasp)
        Note that developer key for Yandex.Rasp is required (stored in .train_api_key)
        Also caches a schedule for today and two days later for faster access
        Key location and cached schedules' files are likely to change in future
"""

import urllib
import json
from urllib import request
from datetime import datetime, timedelta

#: a file containing an API key
API_KEY_FILE = ".train_api_key"

#: URL of train schedule API provider
TRAIN_API_URL = """https://api.rasp.yandex.net/v1.0/search/?apikey={key}\
&format=json&date={date}&from={_from}&to={_to}&lang=ru&transport_types=suburban"""

#: mapping train stations to their API codes
STATIONS = {
    'Одинцово': 'c10743',
    'Кунцево': 's9601728',
    'Фили': 's9600821',
    'Беговая': 's9601666',
    'Белорусская': 's2000006'}


def form_api_url(_from, _to, _timestamp):
    """
        Returns an API url with needed parameters

        Args:
            key(str): API key
            date(datetime): date for schedule
            _from(str): departure train station
            _to(str): arrival train station

        Note:
            `_from` and `_to` should not be equal and should be in STATIONS
    """
    return TRAIN_API_URL.format(
        key=get_key(),
        date=_timestamp.strftime('%Y-%m-%d'),
        _from=STATIONS[_from],
        _to=STATIONS[_to])


def get_key():
    """
        Returns a key(str) as read from file `API_KEY_FILE`
    """
    with open(API_KEY_FILE) as api_key_file:
        key = api_key_file.read()
    return key.strip()


def cache_everything():
    """
        Caches a schedule between all stations
    """
    from itertools import product as P
    for (_from, _to) in P(["Одинцово"], ["Кунцево", "Фили", "Беговая", "Белорусская"]):
        cache_schedule(_from, _to, datetime.now())
        cache_schedule(_to, _from, datetime.now())


def cache_schedule(_from, _to, _timestamp):
    """
        Caches a schedule between stations from arguments starting with certain day
        Writes the cached schedule for day and two days later to train_cached_* files

        Args:
            _from(str): departure train station
            _to(str): arrival train station
            _timestamp(datetime): date to cache schedule for
    """
    schedule_today = json.loads(
        urllib.request.urlopen(form_api_url(
            _from, _to, _timestamp)).read().decode())

    schedule_tomorrow = json.loads(
        urllib.request.urlopen(form_api_url(
            _from, _to, _timestamp+timedelta(days=1))).read().decode())

    schedule_tomorrow2 = json.loads(
        urllib.request.urlopen(form_api_url(
            _from, _to, _timestamp+timedelta(days=2))).read().decode())

    schedule = []
    schedule += schedule_today['threads']
    schedule += schedule_tomorrow['threads']
    schedule += schedule_tomorrow2['threads']

    with open('train_cached_%s_%s' % (STATIONS[_from], STATIONS[_to]), 'w') as cached_schedule_file:
        json.dump(schedule, cached_schedule_file)


def get_schedule(_from, _to, _timestamp):
    """
        Returns a cached schedule between stations in arguments
        If no cached schedule is available, download and return a fresh one

        Args:
            _from(str): departure train station
            _to(str): arrival train station
            _timestamp(datetime): date to get schedule for
    """
    try:
        cached_schedule_file = open('train_cached_%s_%s' % (STATIONS[_from], STATIONS[_to]))
        return json.load(cached_schedule_file)
    except FileNotFoundError:
        cache_schedule(_from, _to, _timestamp)
        return get_schedule(_from, _to, _timestamp)


def get_nearest_train(_from, _to, _timestamp):
    """
        Returns the nearest train

        Args:
            _from(str): place of departure
            _to(str): place of arrival
            _timestamp(datetime): time of departure

        Note:
            `_from` and `_to` should not be equal and should be in STATIONS
    """
    schedule = get_schedule(_from, _to, _timestamp)

    trains = list()
    for train in schedule:
        _train = dict()
        _train['arrival'] = datetime.strptime(
            train['arrival'],
            '%Y-%m-%d %H:%M:%S')
        _train['departure'] = datetime.strptime(
            train['departure'],
            '%Y-%m-%d %H:%M:%S')
        _train['stops'] = train['stops']
        _train['to'] = _to
        _train['title'] = train['thread']['title']
        if _train['departure'] >= _timestamp:
            trains.append(_train)

    delta = timedelta.max

    for train in trains:
        newdelta = train['departure'] - _timestamp
        if newdelta < delta:
            needed_train = train
            delta = newdelta

    return needed_train
