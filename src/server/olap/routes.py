from . import olap
from flask import render_template
from flask import request, jsonify, json, Response
from sqlalchemy.orm.exc import *
from cube.create_cube import *
from cube.model_parse import *


def make_resp(data=None, msg=None, success=True):
    rs = {}
    rs['data'] = data
    rs['msg'] = msg
    rs['success'] = success
    return jsonify(rs)


@olap.route('/')
def index():
    return render_template('index.html', title='KROS')

@olap.route('/dataset/<name>', methods=['POST', 'DELETE', 'PUT'])
def create_dataset(name):
    """
    创建数据集
    :return:
    """
    if request.method == 'POST':
        try:
            try:
                Select_Dataset_By_Name(name=name)
                return make_resp(msg='数据集[{}]已经存在！'.format(name), success=False)
            except NoResultFound as e:
                fact_table = request.form['fact_table']
                lookups = request.form.get('lookups')

                # 创建立方体
                cube_model = create_cube(fact_table, lookups, name)
                cube_json = json.dumps(cube_model)

                id = str(uuid1())
                dataset = Dataset(id=id, name=name)
                cube = Cubes(name=name, name_alias=name, dataset_uuid=id, cube=bytes(cube_json, encoding='utf-8'))
                Inserts(dataset, cube)

                return make_resp(data={'cube':cube_model}, msg='ok')
        except Exception as e:
            return make_resp(msg=str(e), success=False)

    if request.method == 'DELETE':
        try:
            dataset = Select_Dataset_By_Name(name=name)
            id = dataset.id
            Delete_Dataset_By_ID(id, False)
            Delete_Cube_By_ID(id)
            return make_resp(msg='ok')
        except Exception as e:
            rs = make_resp(msg=str(e), success=False)
            return rs

    if request.method == 'PUT':
        try:
            rename = request.form.get('rename')
            fact_table = request.form['fact_table']
            lookups = request.form.get('lookups')

            dataset = Select_Dataset_By_Name(name=name)
            id = dataset.id
            name = rename if rename else name

            Update_Dataset(id, name, commit=False)
            cube_model = create_cube(fact_table, lookups, name)
            cube_json = json.dumps(cube_model)
            Update_Cube(name, name, dataset_uuid=id, cube=bytes(cube_json, encoding='utf-8'), commit=True)

            return make_resp(data={'cube':cube_model}, msg='ok')
        except NoResultFound as e:
            return make_resp(msg='数据集不存在，请先创建数据集.' + str(e), success=False)
        except MultipleResultsFound as e:
            return make_resp(msg='查到多个数据集，' + str(e), success=False)
        except ValueError as e:
            return make_resp(msg='参数错误，' + str(e), success=False)
        except Exception as e:
            return make_resp(msg=str(e), success=False)

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
        cube = Cubes(name='a2', name_alias='a2', dataset_uuid=id, cube=bytes("{}", encoding='utf-8'),
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
