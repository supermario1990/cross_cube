# cude 模型解析

import json
from src.db.model_utils import *

# dims: {"dimensions":[{"table": "mysql_250.sales", "alias":"t_0", "columns":[{"name": "product_id", "alias": "product_id"}]},
#                     {"table": "mysql_250.dates", "alias":"t_1", "columns":[{"name": "date_year", "alias": "YEAR"}]}]}
# measure: {"measures": [{"table": "mysql_250.sales", "alias":"t_0", "column": [{"name": "quantity", "alias": "quantity", "func": "sum"},
# {"name": "price_total", "alias": "price_total", "func": "sum"}]}]}
# filter: {"filter": [{"table": "mysql_250.sales", "alias":"t_0", "columns":[{"name": "product_id", "value": "Sports_Snowboard_table"}]}]}
"""
    dims:
    {
        "dimensions": [
            {
                "table": "mysql_250.sales",
                "alias": "t_0",
                "columns": [
                    {
                        "name": "product_id",
                        "alias": "product_id"
                    }
                ]
            },
            {
                "table": "mysql_250.dates",
                "alias": "t_1",
                "columns": [
                    {
                        "name": "date_year",
                        "alias": "YEAR"
                    }
                ]
            }
        ]
    }
"""
"""
    measures:
    {
        "measures": [
            {
                "table": "mysql_250.sales",
                "alias": "t_0",
                "columns": [
                    {
                        "name": "quantity",
                        "alias": "quantity",
                        "func": "sum"
                    },
                    {
                        "name": "price_total",
                        "alias": "price_total",
                        "func": "sum"
                    }
                ]
            }
        ]
    }
"""
"""
    filter:
    {
        "filter": [
            {
                "table": "mysql_250.sales",
                "alias": "t_0",
                "columns": [
                    {
                        "name": "product_id",
                        "value": "Sports_Snowboard_table"
                    }
                ]
            }
        ]
    }
"""

def generate_select_conditions(dims, measures):
    dims_condition = json.loads(dims)
    measures_condition = json.loads(measures)
    conditions = []
    groups = []
    for i in dims_condition['dimensions']:
        tb = i['alias']
        for co in i['columns']:
            item = tb + '.' + co['name']
            groups.append(item)
            if co['alias'] and len(co['alias']) > 0:
                item = item + ' as ' + co['alias']
            conditions.append(item)

    for i in measures_condition['measures']:
        tb = i['alias']
        for co in i['columns']:
            item = co['func'] + '(' + tb + '.' + co['name']+')'
            if co['alias'] and len(co['alias']) > 0:
                item = item + ' as ' + co['alias']
            conditions.append(item)

    return ','.join(conditions), ','.join(groups)

def generate_filter(filter):
    filter_conditions = json.loads(filter)
    where_list = []
    for i in filter_conditions['filter']:
        tb = i['alias']
        for co in i['columns']:
            item = tb + '.' + co['name'] + ' = ' + '\''+co['value']+'\''
            where_list.append(item)
    return  ' where ' + ','.join(where_list)

def get_full_table(table):
    ds = table.split('.')[0]
    rs = Select_Datasource_By_Name(ds)
    return '.'.join((rs['name'], json.loads(rs['config'])['db_name'])) + '.'+ table.split('.')[1]

def parse(cube_uuid, dims = None, measures = None, filters = None):
    if not cube_uuid:
        return 'no uuid!'
    # 维度和度量必须同时存在，或者同时不存在
    if not dims:
        if measures:
            return 'no dims!'
    if not measures:
        if dims:
            return 'no measures!'

    model_file = 'D:/szkingdomGIT/kros/model/model.json'
    with open(model_file, 'r', encoding='utf-8') as f:
        model = json.load(f)

    print(model)

    fact_tb = get_full_table(model['fact_table'])
    fact_tb_alias = model['alias']

    print('事实表：', fact_tb)
    print('事实表别名:', fact_tb_alias)

    lookups_list = model['lookups']

    join_sql = ''
    for i in lookups_list:
        if i['join']['type'] == 'inner':
            join_sql = join_sql + " inner join "
        elif i['join']['type'] == 'left':
            join_sql = join_sql + " left join "
        else:
            join_sql = join_sql + " right join "

        join_sql = join_sql + get_full_table(i['table']) + ' ' + i['alias'] + ' on ' +\
                   i['join']['foreign_key'] + ' = ' + i['join']['primary_key']


    flat_tb = fact_tb + ' ' + fact_tb_alias + ' '+ join_sql
    select_sql = 'select * from '
    conditions = ''
    groupby = ''
    where = ''

    if dims and measures:
        conditions, groupby = generate_select_conditions(dims, measures)
        select_sql = 'select ' + conditions + ' from '

    if filters:
        where = generate_filter(filters)

    sql = select_sql + flat_tb + where + " group by " + groupby
    #print('sql:', sql)
    return sql

if __name__ == '__main__':
    dims = '{"dimensions":[{"table": "mysql_250.sales", "alias":"t_0", "columns":[{"name": "product_id", "alias": "product_id"}]},{"table": "mysql_250.dates", "alias":"t_1", "columns":[{"name": "date_year", "alias": "YEAR"}]}]}'
    measures = '{"measures": [{"table": "mysql_250.sales", "alias":"t_0", "columns": [{"name": "quantity", "alias": "quantity", "func": "sum"},{"name": "price_total", "alias": "price_total", "func": "sum"}]}]}'
    #filters = '{"filter": [{"table": "mysql_250.sales", "alias":"t_0", "columns":[{"name": "product_id", "value": "Sports_Snowboard_table"}]}]}'
    uuid = '123'
    sql = parse(uuid, dims, measures)
    print(sql)



