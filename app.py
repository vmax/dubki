#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module with Flask web handlers
"""

from flask import Flask, render_template
from flask import request, redirect, json

from route import calculate_route, calculate_route_reverse
from route import DORMS, EDUS
from route_bus import get_nearest_bus
from datetime import datetime, timedelta

from fortune import fortune
from os import environ

import logging

# pythonanywhere

environ['TZ'] = 'Europe/Moscow'

app = Flask(__name__)

VERSION = "VERSION_PLACEHOLDER"


@app.route('/')
def root():
    """
        Root page handler
    """
    dubki_to_odintsovo_bus = get_nearest_bus('Дубки', 'Одинцово', datetime.now())
    odintsovo_to_dubki_bus = get_nearest_bus('Одинцово', 'Дубки', datetime.now())
    context = {
        'dorms': DORMS,
        'edus': EDUS,
        'quote': fortune(),
        'version': VERSION,
        'bus1': dubki_to_odintsovo_bus,
        'bus2': odintsovo_to_dubki_bus
    }
    return render_template('index.html', **context)


class DateTimeAwareJSONEncoder(json.JSONEncoder):
    """
        A JSONEncoder subclass for handling objects of type `timedelta` and `datetime`
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
            }
        elif isinstance(obj, timedelta):
            return {
                '__type__': 'timedelta',
                'days': obj.days,
                'seconds': obj.seconds,
            }
        else:
            return json.JSONEncoder.default(self, obj)


@app.route('/route_json', methods=['POST', 'GET'])
def route_json():
    """
        A function providing JSON API for routing
    """
    if request.method == 'GET':
        pass  # TODO: return an API guide link
    _from = request.form['_from']
    _to = request.form['_to']
    _route = calculate_route(_from, _to, datetime.now(), 'JSON')
    return json.dumps(_route, cls=DateTimeAwareJSONEncoder)


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    """
         A function handling user feedback
    """
    if request.method == 'GET':
        return redirect('/about')
    elif request.method == 'POST':
        with open('feedback.txt', 'a') as feedback_file:
            time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            if request.headers.getlist("X-Forwarded-For"):
                _ip = request.headers.getlist("X-Forwarded-For")[0]
            else:
                _ip = request.remote_addr
                text = request.form['feedback_text']
                feedback_file.write('[%s] -- [%s] -- "%s"\n' % (time, _ip, text))
                return redirect('/')


@app.route('/route', methods=['POST', 'GET'])
def route():
    """
        A function handling the route calculating and displaying
    """
    if request.method == 'GET':
        return redirect('/')
    _from = request.form['_from']
    _to = request.form['_to']

    if request.form.get('date_options') == 'today':
        _ts = datetime.now()
        _tm = [int(x) for x in request.form['time_options'].split(':')]
        _ts = _ts.replace(hour=_tm[0], minute=_tm[1])
        result_route = calculate_route_reverse(_from, _to, _ts)
    elif request.form.get('date_options') == 'tomorrow':
        _ts = datetime.now() + timedelta(days=1)
        _tm = [int(x) for x in request.form['time_options'].split(':')]
        _ts = _ts.replace(hour=_tm[0], minute=_tm[1])
        result_route = calculate_route_reverse(_from, _to, _ts)
    else:
        result_route = calculate_route(_from, _to, datetime.now())

    # if full route takes more than 2.5 hours, consider getting a taxi
    if result_route['full_route_time'].seconds / 3600 > 2.5:
        return render_template('route_taxi.html')

    context = {
        'bus': result_route['bus'],
        'train': result_route['train'],
        'subway': result_route['subway'],
        'onfoot': result_route['onfoot'],
        'arrival': result_route['arrival'],
        'departure': result_route['departure']
    }

    if result_route['departure_place'] == 'dorm':
        context['template_name_or_list'] = 'route_dorm.html'
        context['_from'] = DORMS[_from]
        context['_to'] = EDUS[_to]

    elif result_route['departure_place'] == 'edu':
        context['template_name_or_list'] = 'route_edu.html'
        context['_from'] = EDUS[_from]
        context['_to'] = DORMS[_to]

    return render_template(**context)


@app.route('/about')
def about():
    """
        A function handling `about` page
    """
    return render_template('about.html')


@app.errorhandler(500)
def internal_error(_):
    """
        A function displaying a message in case of error
    """
    return render_template('error-500.html')


@app.before_first_request
def logging_init():
    """
        A function which initializes logging subsystem
    """
    logging.basicConfig(\
            datefmt='%Y-%m-%d %H:%M:%S',\
            format='%(asctime)s%%%(message)s',\
            filename='routing.log',\
            level=logging.CRITICAL)

if __name__ == "__main__":
    app.run(debug=True)
