# 数据库
from sqlalchemy import Column, String, BLOB, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
ModelBase = declarative_base()
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