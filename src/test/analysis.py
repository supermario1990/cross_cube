# 从数据库中加载cube模型，并解析为对应sql

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, BLOB, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from pydrill.client import PyDrill
import json
ModelBase = declarative_base()
engine = create_engine("mysql+pymysql://root:root@192.168.7.250:3306/bi")
class Cubes(ModelBase):
    __tablename__ = 'cubes'
    id = Column(String(length=128), primary_key=True)
    name = Column(String(length=128))
    name_alias = Column(String(length=128))
    datasource_view_id = Column(String(length=128))
    data_model_id = Column(String(length=128))
    cube_dims = Column(BLOB)
    cube_measures = Column(BLOB)
    extends = Column(BLOB)


class DataModel(ModelBase):
    __tablename__ = 'data_model'
    id = Column(String(length=128), primary_key=True)
    name = Column(String(length=128))
    fact_tb = Column(String(length=128))
    relationship = Column(String(length=4096))
    datasource_view_id = Column(String(length=128))
    total_dims = Column(BLOB)
    total_measures = Column(BLOB)

class Datasource(ModelBase):
    __tablename__ = 'datasource'
    id = Column(String(length=128), primary_key=True)
    name = Column(String(length=128))
    type = Column(String(length=64))
    config = Column(String(length=4096))
    test_sql = Column(String(length=512))
    modi_time = Column(TIMESTAMP)

class Datasource_View(ModelBase):
    __tablename__ = 'datasource_view'
    id = Column(String(length=128), primary_key=True)
    name = Column(String(length=1024))

class Logic_tb(ModelBase):
    __tablename__ = 'logic_tb'
    id = Column(String(length=128), primary_key=True)
    name = Column(String(length=128))
    datasource_view_id = Column(String(length=128))
    type = Column(String(length=64))
    datasource_id = Column(String(length=128))
    physical_tb = Column(String(length=4096))
    fields = Column(String(length=4096))


Session = sessionmaker(engine)
session = Session()


# 功能：根据表名查询所属数据源、数据库、物理数据库
# 入参：逻辑表名
# 返回：数据模型ID，数据源名.数据库名.物理数据库
def GetDbName(logic_tb_name):
    for instance in session.query(Logic_tb).filter(Logic_tb.name == logic_tb_name):
        # print(instance.name)
        pass
    id = instance.id
    datasource_id = instance.datasource_id
    physical_tb = instance.physical_tb
    for instance in session.query(Datasource).filter(Datasource.id == datasource_id):
        pass
    source_name = instance.name
    config = json.loads(instance.config)
    db_name = config['db_name']

    return id, source_name + "." + db_name + "." + physical_tb


# 获取表别名
def GetTbAlias(id):
    return 't' + str(id)


# 功能：对立方的关系进行分析
# 入参：事实表，关系
# 返回：join关系
# 说明：立方体一般来说有有两种关系，星型或者雪花模型。此函数将关系模型解析出来。
# 多张表通过关联，汇成一张平表
def AnalysisRelationship(fact_tb, relationship):
    tb_set = set()
    for i in json.loads(relationship)['joins']:
        tb_set.add(i['master'].split('.')[0])

    print(tb_set)
    master_id, full_master_tb = GetDbName(fact_tb)
    full_master_tb_alias = GetTbAlias(master_id)
    json_str = full_master_tb + ' ' + full_master_tb_alias

    def Analysis(fact_tb):
        tmp_str = ""
        master_tb = ""
        for i in json.loads(relationship)['joins']:
            master_tb = i['master'].split('.')[0]
            if master_tb == fact_tb:
                full_master_tb_field = i['master'].replace(master_tb, full_master_tb_alias)
                detail_tb = i['detail'].split('.')[0]
                datail_id, full_detail_tb = GetDbName(detail_tb)
                full_detail_tb_alias = GetTbAlias(datail_id)
                full_detail_tb_field = i['detail'].replace(detail_tb, full_detail_tb_alias)

                # 默认是inner join
                join_type = ' inner join '
                if i['join'] == 'left':
                    join_type = ' left join '
                elif i['join'] == 'right':
                    join_type = ' right join '

                tmp_str = tmp_str + join_type + full_detail_tb + ' ' + full_detail_tb_alias + ' on ' + \
                          full_master_tb_field + " = " + full_detail_tb_field
        return tmp_str

    json_str = json_str + Analysis(fact_tb)
    tb_set.remove(fact_tb)

    for n in tb_set:
        json_str = json_str + Analysis(n)

    return json_str


# demo product, webshop
for instance in session.query(Cubes).filter(Cubes.name == 'product'):
    print(instance.name)

# 获取立方体维度和度量
dims_json = instance.cube_dims
measures_json = instance.cube_measures

dims = json.loads(dims_json)
measures = json.loads(measures_json)

# 获取cube的数据模型信息
data_model_id = instance.data_model_id

for instance in session.query(DataModel).filter(DataModel.id == data_model_id):
    print(instance.name)

# 关联关系
relationship = instance.relationship
fact_tb = instance.fact_tb
if relationship == None or relationship == "" or relationship == '{}':
    print("无关联关系，数据模型为单张逻辑表")
    _, source = GetDbName(fact_tb)
elif relationship.find('joins') != -1:
    print('星型或者雪花模型')
    # 解析join关系
    master_tb = fact_tb
    master_id, full_master_tb = GetDbName(master_tb)
    full_master_tb_alias = GetTbAlias(master_id)
    json_str = full_master_tb + ' ' + full_master_tb_alias
    for i in json.loads(relationship)['joins']:
        full_master_tb_field = i['master'].replace(master_tb, full_master_tb_alias)
        detail_tb = i['detail'].split('.')[0]
        datail_id, full_detail_tb = GetDbName(detail_tb)
        full_detail_tb_alias = GetTbAlias(datail_id)
        full_detail_tb_field = i['detail'].replace(detail_tb, full_detail_tb_alias)
        if i['join'] == 'left':
            tmp_str = ' left join ' + full_detail_tb + ' ' + full_detail_tb_alias + ' on ' +  \
                       full_master_tb_field + " = " + full_detail_tb_field

    source = json_str + tmp_str

print('source: ' + source)

"""
for instance in session.query(Logic_tb).filter(Logic_tb.name == fact_tb):
    print(instance.name)
datasource_id = instance.datasource_id

type = instance.type
if type == 'single':
    source = instance.physical_tb

# 获取数据源信息
for instance in session.query(Datasource).filter(Datasource.id == datasource_id):
    print(instance.name)
    source_name = instance.name
    config = json.loads(instance.config)
    db_name = config['db_name']

    source = source_name + "." + db_name + "." + source

"""

# 条件
print(dims)
print(measures)

condition_dims_str = ",".join(dims['dimensions'])

conditions = []
conditions.append(condition_dims_str)
for i in measures['aggregates']:
    func = i['function']
    tmp = '('+func + '('+i['measure']+')'+')'
    for m in measures['measures']:
        if m['name'] == i['measure']:
            tmp = tmp + ' as ' + m['label'] # measures 中的label作为别名

    conditions.append(tmp)

print(conditions)

condition_str = ",".join(conditions)

sql = 'select ' + condition_str + " from " + source + " group by " + condition_dims_str
print(sql)


# 从drill中查询数据
drill = PyDrill(host='localhost', port=8047)

if not drill.is_active():
    raise ImproperlyConfigured('Please run Drill first')

yelp_reviews = drill.query(sql)

for result in yelp_reviews:
    print(result)