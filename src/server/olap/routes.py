from . import olap
from flask import render_template


@olap.route('/')
def index():
    return render_template('index.html', title='KROS')