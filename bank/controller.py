# -*- coding: utf-8 -*-
from flask import render_template
from bank import app, db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from bank.model import *

# 示例

# 根目录跳转
@app.route('/')
def test():
    return render_template('test.html')