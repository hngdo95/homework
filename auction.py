import datetime
import flask_sqlalchemy
from flask import Flask
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Float, MetaData, Table, DateTime, func ,and_
app=Flask(__name__)
app.config.from_pyfile('config.cfg')
db=SQLAlchemy(app)
association_table = db.Table('user_bid',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('bid_id', db.Integer, db.ForeignKey('bid.id'))
)

class item(db.Model):
    __tablename__ = 'item'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description=Column(String(600), nullable=False)
    start_time=Column(DateTime,default=datetime.datetime.utcnow(),nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))#one to many
    item_bi=relationship('bid',backref='item',lazy=True)#one to many

    def __init__(self, name, user_id,description):
        self.name = name
        self.description=description
        self.user_id = user_id
class bid(db.Model):
    __tablename__ = 'bid'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price=Column(Float,nullable=False)
    item_id=Column(Integer,ForeignKey('item.id'))#one to many
    user_bid = db.relationship("user", secondary=association_table,backref=db.backref('user', lazy='dynamic') )  # many to many
    def __init__(self, price, user_id,item_id):
        self.price=price
        self.user_id=user_id
        self.item_id=item_id
class user(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    user_item = relationship('item',backref='user',lazy=True)  # one to many
    def __init__(self, username, password):
        self.username=username
        self.password=password
db.create_all()
db.session.commit()
