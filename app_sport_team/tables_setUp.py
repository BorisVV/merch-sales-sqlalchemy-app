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

# app = Flask(__name__)
# app.config.from_object('web_config')

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
    sales_of_items = relationship('SalesOfItems', back_populates = 'merchandise_items') #, cascade='all, delete-orphan', passive_deletes = True)
    # # This has a relationship wiht the dates_games table.
    # dates_games = relationship('DatesOfGames', back_populates = 'merchandise_items',\
    #                             cascade='all, delete-orphan', passive_deletes = True)

    def __repr__(self):
        ''' Display the names list'''
        return ' ID = {:<2} {:<2}'.format(self.id, self.item_name.capitalize())



class SalesOfItems(Base):
    ''' This table is for the items sold in each game'''
    __tablename__ = 'sales_of_items'

    id = Column(Integer, primary_key = True)
    item_id = Column(Integer, ForeignKey('merchandise_items.id'))
    date_id = Column(Integer, ForeignKey('games_schedules.id'))
    quantity_sold = Column(Integer, nullable = False)
    price_per_unit = Column(Float(2))


    # total_price = Column(Numeric(12, 2))
    # Relationship setup
    # items_id = Column(Integer, ForeignKey('merchandise_items.id')) # ondelete='CASCADE'
    # merchandise_items = relationship('MerchandiseItems', back_populates='sales_of_items')
    # cascade='all, delete-orphan', single_parent = True, passive_deletes = True)
    # Another option.
    # merchandise_items = relationship('MerchandiseItems', backref=backref('sales_of_items', uselist=True, cascade='delete,all'))

    # tables relations.
    merchandise_items = relationship('MerchandiseItems', back_populates='sales_of_items')
    games_schedules = relationship('DatesOfGames', back_populates='sales_of_items')
    # cascade='all, delete-orphan', single_parent=True, passive_deletes=True)

    def __repr__(self):
        return 'Sales-id: {:<2} qty-sold = {:<4} price = {:<5} total-sale = ${:>6} name-id = {} date-id = {}'\
                .format(self.id, self.quantity_sold, self.price_per_unit, \
                self.total_price, self.items_id, self.dates_id) #self.merchandise_items, self.sales_of_items)


class DatesOfGames(Base):
    ''' This will store hte game's dates table'''
    __tablename__ = 'games_schedules'
    # Add columns
    id = Column(Integer, primary_key = True)
    game_date = Column(Date, unique=True) # Format mm/dd/yyyy
    city = Column(String(50))
    state = Column(String(50))

    sales_of_items = relationship('SalesOfItems', back_populates = 'games_schedules')

    # item_name_id = Column(Integer, ForeignKey('merchandise_items.id'))
    # # Ralashionships with merchandise_items and the sales_of_items tables.
    # merchandise_items = relationship('MerchandiseItems', back_populates = 'dates_games')
    # sales_of_items = relationship('SalesOfItems', back_populates = 'dates_games', cascade='all, delete-orphan', passive_deletes = True)

    def __repr__(self):
        return ' ID = {:}  Date = {:<11} City = {:<12} State = {}  Item_name ID {}'\
        .format(self.id, self.date_of_game, self.city.capitalize(), \
        self.state,  self.item_name_id)

init_db()
