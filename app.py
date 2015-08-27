#!/usr/bin/env python
from flask import Flask,render_template
from flask import request,redirect,json

from route import calculate_route,dorms,edus
from route_bus import get_nearest_bus
from datetime import datetime,timedelta

from fortune import fortune


# pythonanywhere
from os import environ
environ['TZ'] = 'Europe/Moscow'

app = Flask(__name__)


@app.route('/')
def root():
    b1 = get_nearest_bus('Дубки','Одинцово',datetime.now())
    b2 = get_nearest_bus('Одинцово', 'Дубки', datetime.now())
    return render_template('index.html',dorms=dorms, edus=edus, quote=fortune(),bus1=b1,bus2=b2)

class DateTimeAwareJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__' : 'datetime',
                'year' : obj.year,
                'month' : obj.month,
                'day' : obj.day,
                'hour' : obj.hour,
                'minute' : obj.minute,
                'second' : obj.second,
                'microsecond' : obj.microsecond,
            }   
        
        elif isinstance(obj, timedelta):
            return {
                '__type__' : 'timedelta',
                'days' : obj.days,
                'seconds' : obj.seconds,
                'microseconds' : obj.microseconds,
            }
        else:
            return JSONEncoder.default(self, obj)


@app.route('/route_json', methods=['POST','GET'])
def route_json():
    if request.method == 'GET':
        return "There somewhen will be an API guide. Stay tuned. For now you can send me POST-requests with _from and _to params."
    fr = request.form['_from']
    to = request.form['_to']
    return json.dumps(calculate_route(fr,to), cls=DateTimeAwareJSONEncoder)

@app.route('/feedback', methods=['POST','GET'])
def feedback():
        if request.method == 'GET':
                return redirect('/about')
        elif request.method == 'POST':
            with open('feedback.txt','a') as F:
                time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
                ip = request.remote_addr
                text = request.form['feedback_text']
                F.write ('[%s] -- [%s] -- "%s"\n' % (time,ip,text))
                return redirect('/')

@app.route('/route', methods=['POST','GET'])
def route():
        if request.method == 'GET':
                return redirect('/')
        fr = request.form['_from']
        to = request.form['_to']
        route = calculate_route(fr,to)

        # if full route takes more than 2.5 hours, consider getting a taxi
        if route['full_route_time'].seconds / 3600 > 2.5:
            return render_template('route_taxi.html')
            
        if route['departure_place'] == 'dorm':
            return render_template('route_dorm.html', _from=dorms.get(fr), _to=edus.get(to), bus=route['bus'], train=route['train'], subway=route['subway'],onfoot=route['onfoot'],arrival=route['arrival'])
        elif route['departure_place'] == 'edu':
            return render_template('route_edu.html', _from=edus.get(fr), _to=dorms.get(to), bus=route['bus'], train=route['train'], subway=route['subway'],onfoot=route['onfoot'],arrival=route['arrival'])

@app.route('/about')
def about():
	return render_template('about.html')

@app.errorhandler(500)
def internal_error(err):
        return render_template('error-500.html')


if __name__ == "__main__":
	app.run(debug=True)
