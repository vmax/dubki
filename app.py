#!/usr/bin/env python
from flask import Flask,render_template
from flask import request

import route

from datetime import datetime,timedelta
app = Flask(__name__)

dorms = {
    'dubki' : 'Дубки',
}

edus = {
    'aeroport' : 'Кочна',
    'strogino' : 'Строгино',
    'myasnitskaya' : 'Мясо',
    'vavilova' : 'Вавилова',
    'izmailovo' : 'Кирпич',
    'tekstilshiki' : 'Текстильщики'
}


@app.route('/')
def root():
	return render_template('index.html', dorms=dorms, edus=edus)

@app.route('/', methods=['POST'])
def route():
	fr = request.form['_from']
	to = request.form['_to']
	return "%s &rarr; %s" % (fr,to)


if __name__ == "__main__":
	app.run()