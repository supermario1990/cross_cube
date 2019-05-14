# 生成立方体model

from src.db.model_utils import *
import json
import uuid
import time
from pydrill.client import PyDrill

drill = PyDrill(host='localhost', port=8047)

# 参数
# fact_table, lookups
fact_table = 'mysql_250.sales'
lookups = '{"lookups": [{"index": 1,"table": "mysql_250.dates","kind": "LOOKUP","alias": "t_1","join": {"type": "inner","primary_key": "t_1.id","foreign_key": "t_0.date_id"}}]}'
lookups_list = json.loads(lookups)

def all_tbs():
    tbs = []
    tbs.append(fact_table)
    for i in lookups_list['lookups']:
        tbs.append(i['table'])
    return tbs

def get_db(datasource):
    rs = Select_Datasource_By_Name(datasource)
    return '.'.join((rs['name'], json.loads(rs['config'])['db_name']))


def drill_get(sql):

    if not drill.is_active():
        raise ImproperlyConfigured('Please run Drill first')

    yelp_reviews = drill.query(sql)

    return yelp_reviews.rows


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


print(all_tbs())

all_dims = []
all_measures = []

index = 0
for i in all_tbs():
    ds = i.split('.')[0]
    db = get_db(ds)
    tb = i.split('.')[1]

    sql = 'SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = ' + '\'' + tb + '\'' +  'AND TABLE_SCHEMA = ' + '\'' + db + '\''
    print(sql)
    rs = drill_get(sql)

    dims, measures = get_dims_measures(rs)
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
cube_model['name'] = ''
cube_model['description'] = ''
cube_model['alias'] = 't_0'
cube_model['lookups'] = lookups_list['lookups']
cube_model['dimensions'] = all_dims
cube_model['measures'] = all_measures

with open('model.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(cube_model))





