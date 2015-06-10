#!/usr/bin/env python
from flask import Flask,render_template
from flask import request

from route import calculate_route,dorms,edus

from datetime import datetime,timedelta

app = Flask(__name__)


@app.route('/')
def root():
	return render_template('index.html', dorms=dorms, edus=edus, quote=fortune())

@app.route('/route', methods=['POST'])
def route():
        fr = request.form['_from']
        to = request.form['_to']
        route = calculate_route(fr,to)
        return render_template('route.html', _from=dorms.get(fr) or edus.get(fr), _to=dorms.get(to) or edus.get(to), bus=route['bus'], train=route['train'], subway=route['subway'])

@app.route('/about')
def about():
	return render_template('about.html')

def fortune():
    from random import choice
    fortune_quotes = [
        'Дорогу осилит идущий.',
        'Всякому своя дорога.',
        'Одному ехать - и дорога долга.',
        'Где дорога, там и путь.',
        'Не дальняя дорога учит, а ближняя.',
        'Прямая дорога - самая короткая.',
        'По плохой дороге далеко не уедешь.',
        'Дома спи, а в дороге не дремли.',
        'Дорожные люди долго не спят.',
        'Знающий дорогу не устаёт.',
        'Кто знает дорогу, тот не спотыкается.'
    ]
    return choice(fortune_quotes)

if __name__ == "__main__":
	app.run(debug=True)
