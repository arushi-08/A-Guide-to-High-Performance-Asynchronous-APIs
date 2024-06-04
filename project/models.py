from mongoengine import connect

from project import db

connect(
    host="mongodb://flask_celery:flask_celery@mongodb:27017/flask_celery?authSource=admin",
    alias="db",
)


class User(db.Document):
    id = db.IntField()
    username = db.StringField()
    email = db.StringField()
    meta = {"db_alias": "db"}


class Status(db.Document):
    id = db.IntField()
    message = db.StringField()
    state = db.IntField()
    meta = {"db_alias": "db"}
