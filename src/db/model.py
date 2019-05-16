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
    if id == None:
        return None

    try:
        return db.session.query(Dataset).filter(Dataset.id == id).one()
    except Exception as exception:
        print(exception)
        return None


def Insert_Dataset(name, cube_uuid, commit=True):
    '''
    @description: 插入新的数据集信息
    @param {name} {cube_uuid}
    @return:
    '''

    id = str(uuid1())
    if name == None or cube_uuid == None:
        return None

    try:
        New_Dataset = Dataset(
            id=id,
            name=name,
            cube_uuid=cube_uuid)
        db.session.add(New_Dataset)
        if commit:
            db.session.commit()
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
        return db.session.query(Cubes).filter(Cubes.id == id).one()
    except Exception as exception:
        print(exception)
        return None


def Insert_Cube(name, name_alias, cube=None, extends=None, commit=True):
    '''
    @description: 插入新的立方体信息
    @param {name} {name_alias} {cube_info} {extends_info}
    @return:
    '''

    if cube:
        cube = bytes(cube, encoding='utf-8')

    if extends:
        extends = bytes(extends, encoding='utf-8')

    id = str(uuid1())
    try:
        New_Cube = Cubes(
            id=id,
            name=name,
            name_alias=name_alias,
            cube=cube,
            extends=extends)
        db.session.add(New_Cube)
        if commit:
            db.session.commit()
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
        db.session.query(Cubes).filter(Cubes.id == id).delete()
        db.session.commit()
        return True
    except Exception as exception:
        print(exception)
        return False


def Inserts(*args):
    try:
        for i in args:
            db.session.add(i)
        db.session.commit()
        return True
    except Exception as e:
        return False, str(e)
