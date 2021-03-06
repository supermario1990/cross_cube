from . import olap
from flask import render_template
from flask import request, jsonify, json, Response
from sqlalchemy.orm.exc import *
from cube.create_cube import *
from cube.model_parse import *
from drill import drill_utils


def make_resp(data=None, msg=None, success=True):
    rs = {}
    rs['data'] = data
    rs['msg'] = msg
    rs['success'] = success
    return jsonify(rs)

def get_tb_alias(fact_tb, lookups):
    tb_alias = {}
    tb_alias[fact_tb] = 't_0'
    if lookups:
        for i in json.loads(lookups)['lookups']:
            index = 1
            tb_alias[i['table']] = 't_' + str(index)
            index = index + 1
    return tb_alias


def param_check(*args, **kwargs):
    for i in args:
        if i:
            if len(i) == 0:
                raise ValueError('长度不能为0')
    for k, v in kwargs.items():
        if k == 'fact_table':
            if v:
                if len(v.split('.')) != 2:
                    raise ValueError(k + ' 参数格式错误')
        if k == 'lookups':
            if v:
                try:
                    lookups = json.loads(v)
                    if  not 'lookups' in lookups.keys():
                        raise ValueError('缺少lookups关键字')
                    param_list = lookups['lookups']
                    for i in param_list:
                        val1 = ['table', 'alias', 'join']
                        for val in val1:
                            if not val in i.keys():
                                raise ValueError('缺少[{}]关键字'.format(v))

                        val2 = ['type', 'primary_key', 'foreign_key']
                        for val in val2:
                            if not val in i['join'].keys():
                                raise ValueError('缺少[{}]关键字'.format(v))
                except ValueError as e:
                    raise e
                except Exception as e:
                    raise ValueError('参数格式错误，不合法json格式.' + str(e))

        if k in ['dims', 'measures', 'filter']:
            if v:
                try:
                    j = json.loads(v)
                    for val in j.values():
                        val_list = ['table', 'alias', 'columns']
                        for i in val_list:
                            for d in val:
                                if not i in d.keys():
                                    raise ValueError('缺少[{}]关键字'.format(i))

                except ValueError as e:
                    raise e
                except Exception as e:
                    raise ValueError('参数格式错误，不合法json格式.' + str(e))


def update_dims_measuers(dims, measures, model, fact_tb, lookups):
    tb_alias = get_tb_alias(fact_tb, lookups)
    if dims:
        for i in json.loads(dims)['dimensions']:
            alias = tb_alias[i['table']]
            index = 0
            for j in model['dimensions']:
                if alias == j['table']:
                    j['columns'] = i['columns']
                    model['dimensions'][index] = j
                index = index + 1
    if measures:
        for i in json.loads(measures)['measures']:
            alias = tb_alias[i['table']]
            index = 0
            for j in model['measures']:
                if alias == j['table']:
                    j['columns'] = i['columns']
                    model['measures'][index] = j
                index = index + 1

    return model


@olap.route('/')
def index():
    return render_template('index.html', title='KROS')

@olap.route('/dataset/<name>', methods=['GET','POST', 'DELETE', 'PUT'])
def create_dataset(name):
    """
    创建数据集
    :return:
    """
    if request.method == 'GET':
        try:
            dataset = Select_Dataset_By_Name(name=name)
            cube = Select_Cube_By_ID(dataset.id)
            cube_json = str(cube.cube, encoding='utf-8')
            cube_model = json.loads(cube_json)
            return make_resp(data={'cube': cube_model}, msg='ok')
        except NoResultFound as e:
            return make_resp(msg='数据集不存在.' + str(e), success=False)
        except Exception as e:
            return make_resp(msg=str(e), success=False)

    if request.method == 'POST':
        try:
            try:
                Select_Dataset_By_Name(name=name)
                return make_resp(msg='数据集[{}]已经存在！'.format(name), success=False)
            except NoResultFound as e:
                fact_table = request.form['fact_table']
                lookups = request.form.get('lookups')

                param_check(fact_table=fact_table, lookups=lookups)
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
            dims_str = request.form.get('dims')
            measures_str = request.form.get('measures')

            param_check(rename, fact_table=fact_table, lookups=lookups, dims=dims_str, measures=measures_str)

            dataset = Select_Dataset_By_Name(name=name)
            id = dataset.id
            name = rename if rename else name

            Update_Dataset(id, name, commit=False)
            cube_model = create_cube(fact_table, lookups, name)

            cube_model = update_dims_measuers(dims_str, measures_str, cube_model, fact_table, lookups)

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
    :return: 数据集
    """
    if request.method == 'POST':
        try:
            dims = request.form.get('dims')
            measures = request.form.get('measures')
            filter = request.form.get('filter')

            param_check(dims=dims, measures=measures, filter=filter)
            rs = Select_Cube_By_ID(id)
            model = str(rs.cube, encoding='utf-8')
            model = json.loads(model)
            sql = parse(model, dims, measures, filter)
            cellset = json.loads(drill_utils.drill_get(sql))
            cellset['sql'] = sql
            return make_resp(data=cellset, msg='ok')
        except Exception as e:
            return make_resp(msg=str(e), success=False)


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
