import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
metadata=MetaData()
Session = sessionmaker()
session= Session()
association_table = Table('user_bid', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('bid_id', Integer, ForeignKey('bid.id'))
)

class Items(Base):
    __tablename__ = 'item'
    id=Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description=Column(String(600), nullable=False)
    start_time=Column(default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))#one to many
    bid_price = relationship("bid", uselist=False, back_populates="item")#one to one
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    user_item = relationship('item')  # one to many
    user_bid = relationship("User_bid", secondary=association_table)  # many to many
class Bid(Base):
    __tablename__ = 'bid'
    id = Column("id",Integer, primary_key=True, autoincrement=True)
    price=Column(Float,nullable=False)
    item_bid = relationship("item",  back_populates="bid")#one to one

    engine = create_engine('sqlite:///sqlalchemy_example.db')
    Base.metadata.create_all(engine)
