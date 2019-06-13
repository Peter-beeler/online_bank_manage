# -*- coding: utf-8 -*-
from flask import render_template
from bank import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from bank.model import *

# 示例
@app.route('/index', methods=['GET'])

def index():
    return render_template('index.html')
