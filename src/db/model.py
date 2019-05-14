#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, BLOB, TIMESTAMP, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
import os
import json
import datetime

ModelBase = declarative_base()


class Datasource(ModelBase):
    """
    Here you can specify the datasource information for the cubes and build sql query
    """
    __tablename__ = 'datasource'

    id = Column(String(length=128),
                primary_key=True,
                default=lambda: str(uuid4()),
                comment='数据源UUID')
    name = Column(String(length=128), comment='数据源名称')
    type = Column(String(length=64), comment='数据源类型')
    config = Column(String(length=4096), comment='数据源配置')
    test_sql = Column(String(length=512), comment='测试连接SQL语句')
    modi_time = Column(TIMESTAMP,
                       default=datetime.datetime.now(),
                       comment='更新数据源配置时间')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Datasource id: {} name: {} type: {} config: {} test_sql: {}>'.format(self.id, self.name, self.type, self.config, self.test_sql)


class DataSet(ModelBase):
    """
    存储数据集信息，关联立方体。
    """
    __tablename__ = 'data_set'

    id = Column(String(length=128),
                primary_key=True,
                default=lambda: str(uuid4()),
                comment='数据集UUID')
    name = Column(String(length=128), comment='数据集名称')
    cube_uuid = Column(String(length=128),
                       ForeignKey('cubes.id', ondelete='CASCADE'),
                       comment='关联立方体UUID')
    create_time = Column(TIMESTAMP,
                         default=datetime.datetime.now(),
                         comment='创建数据集时间')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<DataSet id: {} name: {} cube_uuid: {}>'.format(self.id, self.name, self.cube_uuid)


class Cubes(ModelBase):
    """
    立方体存储。
    """
    __tablename__ = 'cubes'

    id = Column(String(length=128),
                primary_key=True,
                default=lambda: str(uuid4()),
                comment='立方体UUID')
    name = Column(String(length=128), comment='立方体名称')
    name_alias = Column(String(length=128), comment='立方体别名')
    cube = Column(BLOB, comment='立方体信息')
    extends = Column(BLOB, comment='立方体扩展信息')
    create_time = Column(TIMESTAMP,
                         default=datetime.datetime.now(),
                         comment='创建立方体时间')

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Cubes Name: {} Alias: {} Cube: {} Extends: {}>'.format(self.name, self.name_alias, self.cube, self.extends)


# 如果是从APP.py启动，使用config中配置的URL，如果异常使用绝对配置。
try:
    from config import CONFIG
    config_name = (os.getenv('KROS_CONFIG') or 'default')
    database_uri = CONFIG[config_name].SQLALCHEMY_DATABASE_URI
except Exception as exception:
    database_uri = "mysql+pymysql://root:root@192.168.7.250:3306/kros"
    print(exception)

# TODO
engine = create_engine(database_uri)

# -----------------------------------------------------------------------------------
# 合并model_utils，避免包引用和单独使用存在的问题。
# -----------------------------------------------------------------------------------


class GetSession:
    def __init__(self):
        Session = sessionmaker(engine)
        self.session = Session()

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def Query_Datasource():
    '''
    @description: 查询所有的数据源信息
    @return: 
    '''
    try:
        with GetSession() as session:
            return session.query(Datasource).order_by(Datasource.modi_time).all()
    except Exception as exception:
        print(exception)
        return None


def Select_Datasource_By_ID(id):
    '''
    @description: 根据数据源ID返回数据源信息
    @param {id}
    @return:
    '''
    if id == None:
        return None

    try:
        with GetSession() as session:
            return session.query(Datasource).filter(Datasource.id == id).one()
    except Exception as exception:
        print(exception)
        return None


def Insert_Datasource(name, type, config, test_sql=""):
    '''
    @description: 插入新的数据源配置
    @param {name} {type} {config} {test_sql}
    @return:
    '''
    if name == None or type == None or config == None or test_sql == None:
        return None

    try:
        with GetSession() as session:
            New_Datasource = Datasource(
                name=name,
                type=type,
                config=config,
                test_sql=test_sql)
            session.add(New_Datasource)
            session.commit()
            return New_Datasource.id
    except Exception as exception:
        print(exception)
        return None


def Delete_Datasource_By_ID(id):
    '''
    @description: 根据数据源ID删除对应的数据
    @param {id}
    @return:
    '''
    if id == None:
        return False

    try:
        with GetSession() as session:
            session.query(Datasource).filter(Datasource.id == id).delete()
            session.commit()
            return True
    except Exception as exception:
        print(exception)
        return False


def Query_Dataset():
    '''
    @description: 查询所有的数据集信息
    @return: 
    '''
    try:
        with GetSession() as session:
            return session.query(DataSet).order_by(DataSet.create_time).all()
    except Exception as exception:
        print(exception)
        return None


def Select_Dataset_By_ID(id):
    '''
    @description: 根据数据集ID返回数据集信息
    @param {id}
    @return:
    '''
    if id == None:
        return None

    try:
        with GetSession() as session:
            return session.query(DataSet).filter(DataSet.id == id).one()
    except Exception as exception:
        print(exception)
        return None


def Insert_Dataset(name, cube_uuid):
    '''
    @description: 插入新的数据集信息
    @param {name} {cube_uuid}
    @return:
    '''
    if name == None or cube_uuid == None:
        return None

    try:
        with GetSession() as session:
            New_Dataset = DataSet(
                name=name,
                cube_uuid=cube_uuid)
            session.add(New_Dataset)
            session.commit()
            return New_Dataset.id
    except Exception as exception:
        print(exception)
        return None


def Delete_Dataset_By_ID(id):
    '''
    @description: 根据数据集ID删除对应的数据
    @param {id}
    @return:
    '''
    if id == None:
        return False

    try:
        with GetSession() as session:
            session.query(DataSet).filter(DataSet.id == id).delete()
            session.commit()
            return True
    except Exception as exception:
        print(exception)
        return False


def Query_Cubes():
    '''
    @description: 查询所有的立方体信息
    @return: 
    '''
    try:
        with GetSession() as session:
            return session.query(Cubes).order_by(Cubes.create_time).all()
    except Exception as exception:
        print(exception)
        return None


def Select_Cube_By_ID(id):
    '''
    @description: 根据立方体ID返回立方体信息
    @param {id}
    @return:
    '''
    if id == None:
        return None

    try:
        with GetSession() as session:
            return session.query(Cubes).filter(Cubes.id == id).one()
    except Exception as exception:
        print(exception)
        return None


def Insert_Cube(name, name_alias, cube=None, extends=None):
    '''
    @description: 插入新的立方体信息
    @param {name} {name_alias} {cube_info} {extends_info}
    @return:
    '''
    if cube == None:
        cube = "".encode(encoding='utf-8')
    if extends == None:
        extends = "".encode(encoding='utf-8')

    try:
        with GetSession() as session:
            New_Cube = Cubes(
                name=name,
                name_alias=name_alias,
                cube=cube,
                extends=extends)
            session.add(New_Cube)
            session.commit()
            return New_Cube.id
    except Exception as exception:
        print(exception)
        return None


def Delete_Cube_By_ID(id):
    '''
    @description: 根据立方体ID删除对应的数据
    @param {id}
    @return:
    '''
    if id == None:
        return False

    try:
        with GetSession() as session:
            session.query(Cubes).filter(Cubes.id == id).delete()
            session.commit()
            return True
    except Exception as exception:
        print(exception)
        return False


if __name__ == '__main__':
    # ModelBase.metadata.drop_all(engine)
    # ModelBase.metadata.create_all(engine)
    id = Insert_Datasource('Mysql-250',
                           'mysql',
                           "{\"ip\":\"192.168.7.250\",\"port\":3306,\"user\":\"root\",\"password\":\"root\"}",
                           'SELECT 1')
    id = Insert_Datasource('Mysql-250-2',
                           'mysql',
                           "{\"ip\":\"192.168.7.250\",\"port\":3306,\"user\":\"root\",\"password\":\"root\"}",
                           'SELECT 1')
    print(Query_Datasource())
    print(Select_Datasource_By_ID(id))
    print(Delete_Datasource_By_ID(id))
    print(Select_Datasource_By_ID(id))

    # 外键异常 插入数据集之前，必须先插入立方体
    dataset_id0 = Insert_Dataset('Sales', "0")

    cube_id0 = Insert_Cube(
        "test-cube", "测试立方体0", "{}".encode(encoding='utf-8'), "{}".encode(encoding='utf-8'))
    cube_id1 = Insert_Cube(
        "test-cube", "测试立方体1", "{}".encode(encoding='utf-8'), "{}".encode(encoding='utf-8'))

    print(Query_Cubes())
    print(Select_Cube_By_ID(cube_id1))
    print(Delete_Cube_By_ID(cube_id1))
    print(Select_Cube_By_ID(cube_id1))

    cube_id2 = Insert_Cube("test-cube", "测试立方体2")
    dataset_id1 = Insert_Dataset('Sales', cube_id0)
    dataset_id2 = Insert_Dataset('Sales2', cube_id2)
    print(Query_Dataset())
    print(Select_Dataset_By_ID(dataset_id1))
    print(Delete_Dataset_By_ID(dataset_id2))
    print(Select_Dataset_By_ID(dataset_id2))
