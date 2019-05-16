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
            cube_model = create_cube(fact_table, lookups, name)
            cube_json = json.dumps(cube_model)

            id = str(uuid1())
            dataset = Dataset(id=id, name=name)
            cube = Cubes(name=name, name_alias=name, dataset_uuid=id, cube=bytes(cube_json, encoding='utf-8'))
            Inserts(dataset, cube)
            return jsonify(cube_model)
        except Exception as e:
            return str(e)


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
    """
    测试
    :return:
    """
    try:
        id = str(uuid1())
        dataset = Dataset(id=id, name='a1')
        cube = Cubes(name='a1', name_alias='a1', dataset_uuid=id, cube=bytes("{}", encoding='utf-8'),
              extends=bytes("{}", encoding='utf-8'))
        Inserts(dataset, cube)


        id = str(uuid1())
        dataset = Dataset(id=id, name='a2')
        cude = Cubes(name='a2', name_alias='a2', dataset_uuid=id, cube=bytes("{}", encoding='utf-8'),
              extends=bytes("{}", encoding='utf-8'))
        Inserts(dataset, cube)

        id = str(uuid1())
        dataset = Dataset(id=id, name='a3')
        cube = Cubes(name='a3', name_alias='a3', dataset_uuid=id, cube=bytes("{}", encoding='utf-8'),
              extends=bytes("{}", encoding='utf-8'))
        Inserts(dataset, cube)

        return "ok"
    except Exception as e:
        return str(e)
