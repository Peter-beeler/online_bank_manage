# -*- coding: utf-8 -*-
from flask import render_template
from bank import app, db

# 示例
@app.route('/')
def index():
    return render_template('index.html')
