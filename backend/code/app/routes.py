# -*- coding: utf-8 -*- 
from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'aboba'}
    posts = [
        {
            'author': {'username': 'aboba1'},
            'body': {'GG'}
        },
        {
            'author': {'username': 'aboba2'},
            'body': {'GL'}
        },
        {
            'author': {'username': 'aboba3'},
            'body': {'HF'}
        },
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)