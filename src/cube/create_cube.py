# 生成立方体model

from db.model import *
import uuid
import time
from drill.drill_utils import *
import pysnooper


def all_tbs(fact_table, lookups_list):
    tbs = []
    tbs.append(fact_table)
    if not lookups_list:
        return tbs
    for i in lookups_list['lookups']:
        tbs.append(i['table'])
    return tbs

def get_db(datasource):
    rs = Select_Datasource_By_Name(datasource)
    db_name = '.'.join((rs.name, json.loads(rs.config)['db_name']))
    return db_name

def get_tb_alias(index):
    return 't_' + str(index)

def get_dims_measures(columns):
    num_type = ['INTEGER', 'INT', 'DOUBLE', 'FLOAT']
    dims = []
    measures = []
    for co in columns:
        # measure
        if co['DATA_TYPE'] in num_type:
            measure = {}
            measure['name'] = co['COLUMN_NAME']
            measure['alias'] = ''
            measures.append(measure)
        # dim
        else:
            dim = {}
            dim['name'] = co['COLUMN_NAME']
            dim['alias'] = ''
            dims.append(dim)
    return dims, measures


@pysnooper.snoop()
def create_cube(fact_table, lookups = None, name = None):
    if not fact_table:
        return "fact_table param required!"

    if not lookups:
        lookups_list = None
    else:
        lookups_list = json.loads(lookups)
    print(all_tbs(fact_table, lookups_list))
    all_dims = []
    all_measures = []

    index = 0
    for i in all_tbs(fact_table, lookups_list):
        ds = i.split('.')[0]
        db_name = get_db(ds)
        tb = i.split('.')[1]

        sql = 'SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ' + '\'' + tb + '\'' +  'AND TABLE_SCHEMA = ' + '\'' + db_name + '\''
        print(sql)
        rs = drill_get(sql)

        dims, measures = get_dims_measures(json.loads(rs)['rows'])
        print('dims:', dims)
        print('measures', measures)
        item_dim = {}
        item_dim['table'] = get_tb_alias(index)
        item_dim['columns'] = dims
        all_dims.append(item_dim)

        item_measure = {}
        item_measure['table'] = get_tb_alias(index)
        item_measure['columns'] = measures
        all_measures.append(item_measure)

        index = index + 1

    print('all_dims:', all_dims)
    print('all_measures:', all_measures)

    cube_uuid = uuid.uuid1()
    print(cube_uuid)

    cube_model= {}
    cube_model['uuid'] = str(cube_uuid)
    cube_model['last_modified'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    cube_model['fact_table'] = fact_table
    cube_model['name'] = name
    cube_model['description'] = ''
    cube_model['alias'] = 't_0'
    if lookups_list:
        cube_model['lookups'] = lookups_list['lookups']
    cube_model['dimensions'] = all_dims
    cube_model['measures'] = all_measures

    return cube_model


if __name__ == '__main__':
    # 参数
    # fact_table, lookups
    fact_table = 'mysql_250.sales'
    #lookups = '{"lookups": [{"index": 1,"table": "mysql_250.dates","kind": "LOOKUP","alias": "t_1","join": {"type": "inner","primary_key": "t_1.id","foreign_key": "t_0.date_id"}}]}'

    cube = create_cube(fact_table)
    with open('model.json', 'w', encoding='utf-8') as f:
        f.write(cube)




