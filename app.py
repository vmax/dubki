#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    A module with Flask web handlers
"""

from flask import Flask, render_template, make_response
from flask import request, redirect, json

from route import calculate_route, calculate_route_reverse
from route import DORMS, EDUS
from route_bus import get_nearest_bus
from datetime import datetime, timedelta

from fortune import fortune
from os import environ, chdir

from logger import make_logger
# pythonanywhere

environ['TZ'] = 'Europe/Moscow'

app = Flask(__name__)

VERSION = "VERSION_PLACEHOLDER"

#PYTHONANYWHERE

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
    req_type = request.user_agent.browser and "BROWSER_JSON" or "JSON"
    _route = calculate_route(_from, _to, datetime.now(), req_type)
    return json.dumps(_route, cls=DateTimeAwareJSONEncoder)


@app.route('/route_mobile', methods=['POST'])
def route_mobile():
    """
        A function providing the route for mobile devices

        POST args:
            _from (str): place of departure
            _to (str): place of arrival
            when(str): 'now' | 'today' | 'tomorrow'
            when_param(str): '%H:%M' datetime for reverse routing
            device_id(str): mobile device id for logging

        Returns:
            _route (str): JSON-formatted string with route
    """
    log = make_logger('route_mobile.log')
    _from = request.form['_from']
    _to = request.form['_to']
    when = request.form['when']
    when_param = request.form['when_param']
    device_id = request.form['device_id']
    log("{device_id} {_from} {_to}".format
        (
            device_id=device_id,
            _from=_from,
            _to=_to))
    if when == 'now':
        _route = calculate_route(_from, _to, datetime.now() + timedelta(minutes=10), "MOBILE")
    else:
        _date = datetime.now()
        _time = [int(x) for x in when_param.split(':')]
        _date = _date.replace(hour=_time[0], minute=_time[1])
        if when == 'tomorrow':
            _date += timedelta(days=1)
        _route = calculate_route_reverse(_from, _to, _date)
    js_route = json.dumps(_route, cls=DateTimeAwareJSONEncoder)
    response = make_response(js_route)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route('/feedback', methods=['POST', 'GET'])
def feedback():
    """
         A function handling user feedback
    """
    if request.method == 'GET':
        return redirect('/about')
    elif request.method == 'POST':
        log = make_logger('feedback.log')
        text = request.form['feedback_text']
        log(text)
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

    if not result_route:
        return "Не получилось посчитать маршрут :("

    # if full route takes more than 2.5 hours, consider getting a taxi
    if result_route['full_route_time'].seconds / 3600 > 2.5:
        return render_template('route_taxi.html')

    context = {
        'bus': result_route.get('bus'),
        'train': result_route.get('train'),
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

if __name__ == "__main__":
    app.run(debug=True)
