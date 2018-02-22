import sqlite3
from datetime import date
from sqlalchemy.engine import Engine
from sqlalchemy import ForeignKey,\
                       event,\
                       create_engine,\
                       Column,\
                       Integer,\
                       String,\
                       Float,\
                       Date
from sqlalchemy.orm import relationship,\
                           sessionmaker,\
                           scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask import url_for, Markup

from app_sport_team import app

# This block set up the relationship between tables for the ForeignKey.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
# The scoped_session is good for queries managment.
db_session = scoped_session(sessionmaker(autoflush=False, bind=engine))

def init_db():
    Base.metadata.create_all(bind=engine)

# This set up the Base for the classes, engine to communicate with the db, and Session
# to bind the engine (open and close the sessions.)
Base = declarative_base()
Base.query = db_session.query_property()

class MerchandiseItems(Base):
    ''' This class is for the brand for the merchandises'''
    # Name of table
    __tablename__ = 'merchandise_items'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)

    # This table has a relationship with the sales_of_items table.
    sales_of_items = relationship('SalesOfItems', back_populates = 'merchandise_items')
    # Another option.
    # merchandise_items = relationship('MerchandiseItems', backref=backref('sales_of_items', uselist=True, cascade='delete,all'))
    # cascade='all, delete-orphan', single_parent=True, passive_deletes=True)

    def __repr__(self):
        ''' Display the names list'''
        return '{}'.format(self.name.capitalize())



class SalesOfItems(Base):
    ''' This table is for the items sold in each game'''
    __tablename__ = 'sales_of_items'

    id = Column(Integer, primary_key = True)
    item_id = Column(Integer, ForeignKey('merchandise_items.id'))
    date_id = Column(Integer, ForeignKey('games_schedules.id'))
    quantity_sold = Column(Integer, nullable = False)
    price_per_unit = Column(Float(2))

    # tables relations.
    merchandise_items = relationship('MerchandiseItems', back_populates='sales_of_items') # ondelete='CASCADE'
    games_schedules = relationship('DatesOfGames', back_populates='sales_of_items')

    def __repr__(self):
        return "{} {}".format(self.quantity_sold, self.price_per_unit)


class DatesOfGames(Base):
    ''' This will store the game's dates table'''
    __tablename__ = 'games_schedules'
    # Add columns
    id = Column(Integer, primary_key = True)
    game_date = Column(Date, unique=True) # Format mm/dd/yyyy
    city = Column(String(50))
    state = Column(String(50))

    sales_of_items = relationship('SalesOfItems', back_populates = 'games_schedules')

    def __repr__(self):
        return "{} {} {}".format(self.game_date, self.city, self.state)
init_db()
