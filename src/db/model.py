#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime, BLOB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import datetime
from uuid import uuid4

ModelBase = declarative_base()


class Datasource(ModelBase):
    """
    Here you can specify the datasource information for the cubes and build sql query
    """
    __tablename__ = 'datasource'

    id = Column(String(length=128),
                primary_key=True,
                default=lambda: str(uuid4()),
                comment='uuid')  # TODO  UUID 是否会出现重复问题？
    name = Column(String(length=128), comment='数据源名称')
    type = Column(String(length=64), comment='数据源类型')
    config = Column(String(length=4096), comment='数据源配置')
    test_sql = Column(String(length=512), comment='测试连接SQL语句')
    modi_time = Column(TIMESTAMP, comment='更新数据源配置时间')

    def __repr__(self):
        return '<Datasource %r>' % self.name


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


# -----------------------------------------------------------------------


class DataModel(ModelBase):
    __tablename__ = 'data_model'
    id = Column(String(length=128), primary_key=True)
    name = Column(String(length=128))
    fact_tb = Column(String(length=128))
    relationship = Column(String(length=4096))
    datasource_view_id = Column(String(length=128))
    total_dims = Column(BLOB)
    total_measures = Column(BLOB)


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
