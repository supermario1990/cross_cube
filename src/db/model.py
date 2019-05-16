#!/usr/bin/env python
# -*- coding: utf-8 -*-

from uuid import uuid1
import os
import json
import datetime

from db.db_base import *


def Query_Datasource():
    '''
    @description: 查询所有的数据源信息
    @return: 
    '''
    data = db.session.query(Datasource).order_by(
        Datasource.modi_time).all()
    db.session.close()
    return data


def Select_Datasource_By_ID(id):
    '''
    @description: 根据数据源ID返回数据源信息
    @param {id}
    @return:
    '''
    data = db.session.query(Datasource).filter(
        Datasource.id == id).one()
    db.session.close()
    return data


def Select_Datasource_By_Name(name):
    '''
    @description: 根据数据源名称返回数据源信息
    @param {id}
    @return:
    '''

    try:
        return db.session.query(Datasource).filter(Datasource.name == name).one()
    except Exception as exception:
        print(exception)
        return None


def Insert_Datasource(name, type, config, test_sql, commit=True):
    '''
    @description: 插入新的数据源配置
    @param {name} {type} {config} {test_sql}
    @return:
    '''
    New_Datasource = Datasource(
        id=str(uuid1()),
        name=name,
        type=type,
        config=config,
        test_sql=test_sql)
    db.session.add(New_Datasource)
    if commit:
        db.session.commit()
    return New_Datasource.id


def Update_Datasource(id, name, type, config, test_sql, commit=True):
    '''
    @description: 更新数据源配置
    @param {id} {name} {type} {config} {test_sql}
    @return:
    '''
    db.session.query(Datasource).filter(
        Datasource.id == id).update(
            {
                'id': id,
                'name': name,
                'type': type,
                'config': config,
                'test_sql': test_sql
            })
    if commit:
        db.session.commit()
    return id


def Delete_Datasource_By_ID(id, commit=True):
    '''
    @description: 根据数据源ID删除对应的数据
    @param {id}
    @return:
    '''
    db.session.query(Datasource).filter(Datasource.id == id).delete()
    if commit:
        db.session.commit()
    return True


def Delete_Datasource_By_Name(name):
    '''
    @description: 根据数据源名称删除对应的数据
    @param {name}
    @return:
    '''
    if name == None:
        return False

    try:
        db.session.query(Datasource).filter(Datasource.name == name).delete()
        db.session.commit()
        return True
    except Exception as exception:
        print(exception)
        db.session.rollback()
        return False


def Query_Dataset():
    '''
    @description: 查询所有的数据集信息
    @return: 
    '''
    try:
        return db.session.query(Dataset).order_by(Dataset.create_time).all()
    except Exception as exception:
        print(exception)
        return None


def Select_Dataset_By_ID(id):
    '''
    @description: 根据数据集ID返回数据集信息
    @param {id}
    @return:
    '''
    if not id:
        raise ValueError('id param required')

    try:
        return db.session.query(Dataset).filter(Dataset.id == id).one()
    except Exception as e:
        db.session.rollback()
        raise e


def Insert_Dataset(name, commit=True):
    '''
    @description: 插入新的数据集信息
    @param {name} {cube_uuid}
    @return:
    '''

    id = str(uuid1())
    if not name:
        raise ValueError('name param required')

    try:
        New_Dataset = Dataset(
            id= id,
            name=name
            )
        db.session.add(New_Dataset)
        if commit:
            db.session.commit()
        return New_Dataset.id
    except Exception as e:
        db.session.rollback()
        raise e


def Delete_Dataset_By_ID(id):
    '''
    @description: 根据数据集ID删除对应的数据
    @param {id}
    @return:
    '''
    if id == None:
        return False

    try:
        db.session.query(Dataset).filter(Dataset.id == id).delete()
        db.session.commit()
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
        db.session.query(Cubes).order_by(Cubes.create_time).all()
    except Exception as e:
        db.session.rollback()
        raise e


def Select_Cube_By_ID(id):
    '''
    @description: 根据立方体ID返回立方体信息
    @param {id}
    @return:
    '''
    if not id:
        raise ValueError('id param required')

    try:
        return db.session.query(Cubes).filter(Cubes.dataset_uuid == id).one()
    except Exception as e:
        db.session.rollback()
        raise e


def Insert_Cube(name, name_alias, dataset_uuid, cube=None, extends=None, commit=True):
    '''
    @description: 插入新的立方体信息
    @param {name} {name_alias} {cube_info} {extends_info}
    @return:
    '''
    if not name or not name_alias or not dataset_uuid:
        raise ValueError('wrang income params')

    if cube:
        cube = bytes(cube, encoding='utf-8')

    if extends:
        extends = bytes(extends, encoding='utf-8')

    try:
        New_Cube = Cubes(
            name=name,
            name_alias=name_alias,
            dataset_uuid=dataset_uuid,
            cube=cube,
            extends=extends)
        db.session.add(New_Cube)
        if commit:
            db.session.commit()
        return New_Cube.id
    except Exception as e:
        db.session.rollback()
        raise e


def Delete_Cube_By_ID(id):
    '''
    @description: 根据立方体ID删除对应的数据
    @param {id}
    @return:
    '''
    if id == None:
        raise ValueError('id param required')

    try:
        db.session.query(Cubes).filter(Cubes.id == id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e


def Inserts(*args):
    try:
        for i in args:
            db.session.add(i)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e


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
