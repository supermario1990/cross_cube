"""
db_base.py

定义数据库结构
"""
from server import db

class Cubes(db.Model):
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), index=True, unique=True)
    name_alias = db.Column(db.String(128), index=True, unique=True)
    dataset_uuid = db.Column(db.String(128))
    cube = db.Column(db.LargeBinary)
    extends = db.Column(db.LargeBinary)
    modi_time = db.Column(db.TIMESTAMP, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Cubes Name: {} Alias: {} Cube: {} Extends: {}>'.format(self.name, self.name_alias, self.cube, self.extends)

class Dataset(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    modi_time = db.Column(db.TIMESTAMP, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<DataSet id: {} name: {} cube_uuid: {}>'.format(self.id, self.name, self.cube_uuid)


class Datasource(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    type = db.Column(db.String(64))
    config = db.Column(db.String(4096))
    test_sql = db.Column(db.String(512))
    modi_time = db.Column(db.TIMESTAMP, nullable=False)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Datasource id: {} name: {} type: {} config: {} test_sql: {}>'.format(self.id, self.name, self.type, self.config, self.test_sql)
