#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module which calculates the onfoot time (using precomputed values)
"""

from datetime import timedelta

#: IDs for maps showing onfoot route
MAP_SOURCES = {
    'aeroport': '9kfYmO7lbg2o_YuSTvZqiY9rCevo23cs',
    'gnezdo': '_a_UjKz_rMbmf2l_mWtsRUjlaqlRySIS',
    'hitra': 'j1cHqL5k2jw_MK31dlBLEwPPPmj72NNg',
    'ilyinka': '7UEkPE7kT0Bhb4rOzDbk2O57LdWBE8Lq',
    'izmailovo': 'tTSwzei04UwodpOe5ThQSKwo47ZiR8aO',
    'myasnitskaya': 'GGWd7qLfRklaR5KSQQpKFOiJT8RPFGO-',
    'paveletskaya': '1SimW8pYfuzER0tbTEYFs1RFaNUFnhh-',
    'petrovka': 'pSiE6gI2ftRfAGBDauSW0G0H2o9R726u',
    'shabolovskaya': '0enMIqcJ_dLy8ShEHN34Lu-4XBAHsrno',
    'st_basmannaya': 'LwunOFh66TXk8NyRAgKpsssV0Gdy34pG',
    'strogino': 'pMeBRyKZjz3PnQn4HCZKIlagbMIv2Bxp',
    'tekstilshiki': 'IcVLk9vNC1afHy5ge05Ae07wahHXZZ7H',
    'trehsvyat_b': '_WWkurGGUbabsiPE9xgdLP_iJ61vbJrZ',
    'trehsvyat_m': 'jBGwqmV8V-JjFzbG2M_13sGlAUVqug-9',
    'vavilova': '_Cz-NprpRRfD15AECXvyxGQb5N7RY3xC',
    'ordynka': 'SpOVmas47ctXFTbX9GdKarOc1XvWiART'
    }

#: onfoot times
DELTAS = {
    'aeroport': timedelta(minutes=14),
    'strogino': timedelta(minutes=6),
    'tekstilshiki': timedelta(minutes=10),
    'st_basmannaya': timedelta(minutes=16),
    'vavilova': timedelta(minutes=5),
    'myasnitskaya': timedelta(minutes=6),
    'izmailovo': timedelta(minutes=16),
    'shabolovskaya': timedelta(minutes=5),
    'petrovka': timedelta(minutes=6),
    'paveletskaya': timedelta(minutes=5),
    'ilyinka': timedelta(minutes=7),
    'trehsvyat_b': timedelta(minutes=13),
    'trehsvyat_m': timedelta(minutes=15),
    'hitra': timedelta(minutes=13),
    'gnezdo': timedelta(minutes=5),
    'ordynka': timedelta(minutes=5)
    }


def form_map_url(edu, url_type='static'):
    """
        Returns a map url for displaying in a webpage

        Args:
            edu(str): which education campus the route's destination is
            url_type(Optional[str]): whether the map should be interactive

        Note:
            `edu` should be a value from EDUS
            `url_type` should be in {'static', 'js'}
    """
    base_url = 'https://api-maps.yandex.ru/services/constructor/1.0/%s/?sid=%s'
    return base_url % (url_type, MAP_SOURCES[edu])


def get_nearest_onfoot(edu, _timestamp):
    """
        Returns the nearest onfoot route

        Args:
            edu(str): place of arrival
            _timestamp(datetime): time of departure from subway exit

        Note:
            `edu` should be a value from EDUS
    """
    result = dict()
    result['departure'] = _timestamp
    result['mapsrc'] = form_map_url(edu)
    result['time'] = DELTAS[edu]
    result['arrival'] = result['departure'] + result['time']
    return result
