

from sqlalchemy import ForeignKey, event, create_engine, Column,\
                    Integer, String, Numeric, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship, sessionmaker, backref
from exceptions import ValueError


# This block set up the relationship between tables.
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# This set up the Base for the classes, engine to communicate with the db, and Session
# to bind the engine (open and close the sessions.)
Base = declarative_base()
engine = create_engine('sqlite:///merchandise_sales.db', echo = False)
Session = sessionmaker(bind=engine) # Helps set up the database.

class MerchandiseItems(Base):
    ''' This class is for the  for the merchandises'''
    # Name of table
    __tablename__ = 'merchandise'
    id = Column(Integer, primary_key = True)
    item_name = Column(String(50), nullable = False) # example shoes

    # This table has a relationship with the sales_of_items table.
    sales_of_items = relationship('SalesOfItems', back_populates = 'merchandise_items', cascade='delete,all')
    # This has a relationship wiht the dates_games table.
    dates_games = relationship('DatesOfGames', back_populates = 'merchandise_items', cascade='delete,all')

    def __repr__(self):
        ''' Display the names list'''
        return ' ID = {:<2} {:<2}'.format(self.id, self.item_name.capitalize())



class SalesOfItems(Base):
    ''' This table is for the items sold in each game'''
    __tablename__ = 'sales_of_items'

    id = Column(Integer, primary_key = True)
    quantity_sold = Column(Integer, nullable = False)
    price_per_unit = Column(Numeric(12, 2))
    total_price = Column(Numeric(12, 2))

    # Relationship setup
    items_id = Column(Integer, ForeignKey('merchandise_items.id'))
    merchandise_items = relationship('MerchandiseItems', back_populates = 'sales_of_items', cascade='delete,all')
    # merchandise_items = relationship('MerchandiseItems', backref=backref('sales_of_items', uselist=True, cascade='delete,all'))

    dates_id = Column(Integer, ForeignKey('dates_games.id'))
    # This table has a relationship wiht the dates_games table.
    dates_games = relationship('DatesOfGames', back_populates = 'sales_of_items')

    def __repr__(self):
        return 'Sales-id: {:<2} qty-sold = {:<4} price = {:<5} total-sale = ${:>6} name-id = {} date-id = {}'\
                .format(self.id, self.quantity_sold, self.price_per_unit, \
                self.total_price, self.items_id, self.dates_id) #self.merchandise_items, self.sales_of_items)


class DatesOfGames(Base):
    ''' This will store hte game's dates table'''
    __tablename__ = 'dates_games'
    # Add columns
    id = Column(Integer, primary_key = True)
    date_of_game = Column(String(20), nullable = False) # Format mm/dd/yyyy
    city = Column(String(50), nullable = False)
    state = Column(String(50), nullable = False)

    # sales_id = Column(Integer, ForeignKey('sales_of_items.id'))

    item_name_id = Column(Integer, ForeignKey('merchandise_items.id'))
    # Ralashionships with merchandise_items and the sales_of_items tables.
    merchandise_items = relationship('MerchandiseItems', back_populates = 'dates_games')
    sales_of_items = relationship('SalesOfItems', back_populates = 'dates_games')


    # sales_of_items = relationship('SalesOfItems', back_populates = 'dates_games')
    def __repr__(self):
        return ' ID = {:}  Date = {:<11} City = {:<12} State = {}  Item_name ID {}'\
        .format(self.id, self.date_of_game, self.city.capitalize(), \
        self.state,  self.item_name_id)


Base.metadata.create_all(engine)
