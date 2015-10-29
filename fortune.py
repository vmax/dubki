#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module providing a quote for index page
    Quotes are gathered from random folklore sources from the Web
"""

from random import choice

#: Set of quotes to choose from
FORTUNE_QUOTES = (
    'Большая дорога начинается с первого шага.',
    'В дороге и отец сыну товарищ.',
    'В игре да в попутье людей узнают.',
    'В темную ночь дорога далека.',
    'Всякому своя дорога.',
    'Где дорога, там и путь.',
    'Долог путь, да изъездчив.',
    'Дома спи, а в дороге не дремли.',
    'Домашняя дума в дорогу не годится.',
    'Дорога даже в ухабах лучше бездорожья.',
    'Дорога, по которой ходили тысячу лет, превращается в реку.',
    'Дорогу выбирай любую, а родную страну не забывай.',
    'Дорогу осилит идущий.',
    'Дорожные люди долго не спят.',
    'Знающий дорогу не устаёт.',
    'Идущий дорогу одолевает, сидящего думы одолевают.',
    'Идущий любую дорогу осилит.',
    'Каков поехал, таков и приехал.',
    'Кто знает дорогу, тот не спотыкается.',
    'Лучше плохая дорога, чем плохой попутчик.',
    'Настойчивый дорогу осилит.',
    'Не дальняя дорога учит, а ближняя.',
    'Не хвались отъездом, хвались приездом..',
    'Незнакомая дорога подобна яме.',
    'Ночь, как день; дорога, как скатерть - садись да катись!',
    'Одному ехать - и дорога долга.',
    'Открытому сердцу дорога открыта.',
    'Пешечком верней будешь.',
    'По плохой дороге далеко не уедешь.',
    'Прямая дорога - самая короткая.',
    'Слабые ноги крепнут в дороге.',
    'Тело довезу, а за душу не ручаюсь.',
    'Уступай дорогу дуракам и сумасшедшим.',
    'Что найти суждено - на дороге лежит.',
    'Шибко ехать - не скоро доехать.')


def fortune():
    """Returns a random quote for index page"""
    return choice(FORTUNE_QUOTES)
