
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, \
String, DateTime, \
ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# from flask_sqlalchemy import SQLAlchemy
# from flask import url_for
# from app_sport_team import app
# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True, \
#                     **app.config['SQLALCHEMY_DATABASE_CONNECT_OPTIONS'])   # TODO: Remove **app.conf...
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))
# def init_db():
#     Model.metadata.create_all(bind=engine)
# Model = declarative_base(name='Model')
# Model.query = db_session.query_property()

engine = create_engine("sqlite:///sportgoods.db")
Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    price = Column(Float)

    def __repr__(self):
        return "<Item(name='%s', price='%.2f')>" % (self.name, self.price)

# class Schedule(Base):
#     __tablename__ = 'schedules'
#     id = Column('schedule_id', Integer, primary_key=True)
#     city = Column(String(50))
#     state = Column(String(2))
#     game_date = Column(DateTime)
#
#
# class Quantitysold(Base):
#     __tablename__ = 'quantities'
#     id = Column('quantities_id', Integer, primary_key=True)
#     item_id = Column(Integer, ForeignKey('items.'))
#     game_date_id = Column(Integer, ForeignKey('schedule.id'))
#     quantity = Column(Integer)
#
#     item = relation(Item, backref=backref('items', lazy=True))
#     schedule = relation(Schedule, backref=backref('schedules'))
#
#     def __init__(self, quantity):
#         self.quantity = quantity

# event.listen(db_session, 'after_flush', search.update_model_based_indexes)
