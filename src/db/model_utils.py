from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from pydrill.client import PyDrill
import json
from src.db.model import *

engine = create_engine("mysql+pymysql://root:root@192.168.7.250:3306/kros")
#Session = sessionmaker(engine)
#session = Session()


class getSession:
    def __init__(self):
        Session = sessionmaker(engine)
        self.session = Session()
    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

def Select_Cubes_By_Name(name):
    with getSession() as session:
        instance = session.query(Cubes).filter(Cubes.name == name).one()
        rs = {}
        rs['id'] = instance.id
        rs['name'] = instance.name
        rs['name_alias'] = instance.name_alias
        rs['datasource_view_id'] = instance.datasource_view_id
        rs['data_model_id'] = instance.data_model_id
        rs['cube_dims'] = instance.cube_dims
        rs['cube_measures'] = instance.cube_measures
        rs['extends'] = instance.extends
        return rs


def Select_DataModel_By_ID(id):
    with getSession() as session:
        instance = session.query(DataModel).filter(DataModel.id == id).one()
        rs = {}
        rs['id'] = instance.id
        rs['name'] = instance.name
        rs['fact_tb'] = instance.fact_tb
        rs['relationship'] = instance.relationship
        rs['datasource_view_id'] = instance.datasource_view_id
        rs['total_dims'] = instance.total_dims
        rs['total_measures'] = instance.total_measures
        return rs


def Select_Logictb_by_name(name):
    with getSession() as session:
        instance = session.query(Logic_tb).filter(Logic_tb.name == name).one()
        rs = {}
        rs['id'] = instance.id
        rs['name'] = instance.name
        rs['type'] = instance.type
        rs['datasource_id'] = instance.datasource_id
        rs['datasource_view_id'] = instance.datasource_view_id
        rs['physical_tb'] = instance.physical_tb
        rs['fields'] = instance.fields
        return rs


def Select_Datasource_By_ID(id):
    with getSession() as session:
        instance = session.query(Datasource).filter(Datasource.id == id).one()
        rs = {}
        rs['id'] = instance.id
        rs['name'] = instance.name
        rs['type'] = instance.type
        rs['config'] = instance.config
        rs['test_sql'] = instance.test_sql
        rs['modi_time'] = instance.modi_time
        return rs

def Select_Datasource_By_Name(name):
    with getSession() as session:
        instance = session.query(Datasource).filter(Datasource.name == name).one()
        rs = {}
        rs['id'] = instance.id
        rs['name'] = instance.name
        rs['type'] = instance.type
        rs['config'] = instance.config
        rs['test_sql'] = instance.test_sql
        rs['modi_time'] = instance.modi_time
        return rs


# 功能：根据表名查询所属数据源、数据库、物理数据库
# 入参：逻辑表名
# 返回：数据模型ID，数据源名.数据库名.物理数据库
def GetDbName(logic_tb_name):
    logic_rs = Select_Logictb_by_name(logic_tb_name)
    id = logic_rs['id']
    datasource_id = logic_rs['datasource_id']
    physical_tb = logic_rs['physical_tb']

    ds_rs = Select_Datasource_By_ID(datasource_id)
    source_name = ds_rs['name']
    config = json.loads(ds_rs['config'])
    db_name = config['db_name']

    return id, source_name + "." + db_name + "." + physical_tb


if __name__ == '__main__':
    print('model utils')
    print(Select_Cubes_By_Name('dates'))