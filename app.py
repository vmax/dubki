#!/usr/bin/env python
from flask import Flask,render_template
from flask import request,redirect,json

from route import calculate_route,dorms,edus
from route_bus import get_nearest_bus
from datetime import datetime,timedelta


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


@app.route('/route_json', methods=['POST'])
def route_json():
    fr = request.form['_from']
    to = request.form['_to']
    return json.dumps(calculate_route(fr,to), cls=DateTimeAwareJSONEncoder)



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
            return render_template('route_dorm.html', _from=dorms.get(fr), _to=edus.get(to), bus=route['bus'], train=route['train'], subway=route['subway'])
        elif route['departure_place'] == 'edu':
            return render_template('route_edu.html', _from=edus.get(fr), _to=dorms.get(to), bus=route['bus'], train=route['train'], subway=route['subway'])

@app.route('/about')
def about():
	return render_template('about.html')


def fortune():
    from random import choice
    fortune_quotes = [
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
'Шибко ехать - не скоро доехать.'
    ]
    return choice(fortune_quotes)

@app.errorhandler(500)
def internal_error(err):
        return render_template('error-500.html')


if __name__ == "__main__":
	app.run(debug=True)
