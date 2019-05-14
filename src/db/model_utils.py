#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
import json
import os
from config import CONFIG
from .model import *  # TODO 从app.py启动程序

config_name = (os.getenv('KROS_CONFIG') or 'default')
DATABASE_URI = CONFIG[config_name].SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI)


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
    '''
    @description: 根据数据源ID返回数据源信息
    @param {id} 
    @return: 
    '''
    if id == None:
        return None

    rs = {}
    try:
        with getSession() as session:
            instance = session.query(Datasource).filter(
                Datasource.id == id).one()
            rs['id'] = instance.id
            rs['name'] = instance.name
            rs['type'] = instance.type
            rs['config'] = instance.config
            rs['test_sql'] = instance.test_sql
            rs['modi_time'] = instance.modi_time
            return rs
    except Exception as exception:
        return None
    return rs


def Insert_Datasource(name, type, config, test_sql):
    '''
    @description: 插入新的数据源配置
    @param {name} {type} {config} {test_sql}
    @return: 
    '''
    if name == None or type == None or config == None or test_sql == None:
        return False

    try:
        with getSession() as session:
            New_Datasource = Datasource(
                name=name,
                type=type,
                config=config,
                test_sql=test_sql)
            session.add(New_Datasource)
            session.commit()
    except Exception as exception:
        return False
    return True


def Delete_Datasource_By_ID(id):
    '''
    @description: 根据数据源ID删除对应的数据
    @param {id} 
    @return: 
    '''


def Select_Datasource_By_Name(name):
    with getSession() as session:
        instance = session.query(Datasource).filter(
            Datasource.name == name).one()
        rs = {}
        rs['id'] = instance.id
        rs['name'] = instance.name
        rs['type'] = instance.type
        rs['config'] = instance.config
        rs['test_sql'] = instance.test_sql
        rs['modi_time'] = instance.modi_time
        return rs


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
