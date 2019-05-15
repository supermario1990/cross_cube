from . import olap
from flask import render_template
from db.model import *


@olap.route('/')
def index():
    return render_template('index.html', title='KROS')

@olap.route('/dataset', methods=['POST'])
def create_dataset():
    """
    创建数据集
    :return:
    """
    return "ok"