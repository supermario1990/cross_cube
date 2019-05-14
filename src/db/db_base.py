from server import db

class Cubes(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    name_alias = db.Column(db.String(128), index=True, unique=True)
    cube = db.Column(db.LargeBinary)
    extends = db.Column(db.LargeBinary)


class Dataset(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    cube_uuid = db.Column(db.String(128), index=True, unique=True)


class Datasource(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    type = db.Column(db.String(64), index=True, unique=True)
    config = db.Column(db.String(4096))
    test_sql = db.Column(db.String(512))
    modi_time = db.Column(db.TIMESTAMP)
