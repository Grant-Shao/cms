# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DB_URI = "mysql+pymysql://root:root@127.0.0.1:3306/xiachufang2"
engine = create_engine(DB_URI)
Base = declarative_base(engine)
session = sessionmaker(engine)()

class Recipe_Mat(Base):
    __tablename__ = 'recipe_mat'
    material_id = Column(Integer, ForeignKey('material.id'),primary_key=True)
    food_id = Column(Integer, ForeignKey('food.id'),primary_key=True)

class Recipe(Base):
    __tablename__='food'
    id=Column(Integer,autoincrement=True,primary_key=True)
    food=Column(String(128),nullable=False)
    step=Column(Text)
    tip=Column(Text)
    description=Column(Text)
    materials=relationship('Material',secondary='recipe_mat')


class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, autoincrement=True, primary_key=True)
    material = Column(String(128), nullable=False)
    volume=Column(String(128))
    foods = relationship('Recipe', secondary='recipe_mat')

# Base.metadata.create_all()
# title = 'title t333332'
# description = 'description3333 test'
# tip = 'tip33333 testing'
#
# stuff = {
#     '张三':'1个',
#     '李四':'2个',
#     '王五':'n个'
# }
#
# steps = 'step1, test1, \n step2, test2 \n step3, test3'
#
# data=Recipe(
#     food=title,
#     description=description,
#     tip=tip,
#     step=steps
# )
# session.add(data)
# session.commit()
#
#
# for k,v in list(stuff.items()):
#     mat=Material(
#         material=k,
#         volume=v
#     )
#     mat.foods = [data]
#     session.add(mat)
#
#     session.commit()