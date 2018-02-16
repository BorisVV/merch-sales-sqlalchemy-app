
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float, \
String, DateTime, \
ForeignKey, \
Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
Session = sessionmaker(bind=engine)
    # If the engine was not created previus to the above line, then the option
    # is to do the <Session = sessionmaker()> and later use the <Session.configure(bind=engine)>
session = Session() # instance of Session()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence("item_id_seq"), primary_key=True)
    name = Column(String(80))
    price = Column(Float)

    def __repr__(self):
        return "<Item(name='%s', price='%.2f')>" % (self.id, self.name, self.price)

class Quantitysold(Base):
    __tablename__ = 'quantities'
    id = Column('quantities_id', Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)

    item = relationship("Item", back_populates='quantities')

    def __repr__(self):
        return "<Quantitysold(id='{}', item_id='{}', quantity='{}')>" \
        .format(self.id, self.item_id, self.quantity)

Item.quantities = relationship("Quantitysold", back_populates="item")

Base.metadata.create_all(engine)
# class Schedule(Base):
#     __tablename__ = 'schedules'
#     id = Column('schedule_id', Integer, primary_key=True)
#     city = Column(String(50))
#     state = Column(String(2))
#     game_date = Column(DateTime)
#
#

# event.listen(db_session, 'after_flush', search.update_model_based_indexes)
