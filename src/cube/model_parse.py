# cude 模型解析

import json


model_file = 'D:/szkingdomGIT/kros/model/model.json'

with open(model_file, 'r', encoding='utf-8') as f:
    model = json.load(f)

print(model)

fact_tb = model['fact_table']
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

    join_sql = join_sql + i['table'] + ' ' + i['alias'] + ' on ' +\
               i['join']['foreign_key'] + ' = ' + i['join']['primary_key']


flat_tb = fact_tb + ' ' + fact_tb_alias + ' '+ join_sql

sql = 'select * from ' + fact_tb + ' ' + fact_tb_alias + ' '+ join_sql
print('sql:', sql)




