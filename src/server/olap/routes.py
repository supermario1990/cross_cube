from . import olap
from flask import render_template
from flask import request, jsonify, json
from cube.create_cube import *
from cube.model_parse import *


@olap.route('/')
def index():
    return render_template('index.html', title='KROS')

@olap.route('/dataset/<name>', methods=['POST'])
def create_dataset(name):
    """
    创建数据集
    :return:
    """
    if request.method == 'POST':
        try:
            fact_table = request.form['fact_table']
            lookups = request.form.get('lookups')

            # 创建立方体
            cube = create_cube(fact_table, lookups, name)
            cube_json = json.dumps(cube)
            cube_id = Insert_Cube(name, name, cube_json, None, commit=True)
            dataset_id = Insert_Dataset(name, cube_id, commit=True)
            return jsonify(cube)
        except Exception as e:
            return e


@olap.route('/cube/<id>', methods=['POST'])
def query_cude(id):
    """
    根据cude查询数据
    :param id:
    :return:
    """
    try:
        dims = request.form.get('dims')
        measures = request.form.get('measures')
        filter = request.form.get('filter')

        rs = Select_Cube_By_ID(id)
        model = str(rs.cube, encoding='utf-8')
        model = json.loads(model)
        sql = parse(model, dims, measures, filter)
        return sql
    except Exception as e:
        return str(e)


@olap.route('/test')
def test():
    id = str(uuid1())
    Dataset(id, name='a1')
    Cubes(name='a1', name_alias='a1', )

    id = str(uuid1())
    Dataset(id, name='a2')