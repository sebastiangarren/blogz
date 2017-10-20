from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app, db


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))

    def __init__(self,username,password):
        self.username = username
        self.password = password

class Blog_post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def __init__(self, title, body, author_id, datetime):
        self.title = title
        self.body = body
        self.author_id = author_id
        if datetime is None:
            datetime = datetime.utcnow()
        self.datetime = datetime

    def __repr__(self):
        return '<Blog_post %r>' % self.title