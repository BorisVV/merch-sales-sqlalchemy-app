

from sqlalchemy import ForeignKey, event, create_engine, Column,\
                    Integer, String, Numeric, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship, sessionmaker



@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

Base = declarative_base()
engine = create_engine('sqlite:///merchandise_sales.db', echo = False)
Session = sessionmaker(bind=engine) # Helps set up the database.


class MerchandiseItems(Base):
    ''' This class is for the brand for the merchandises'''
    # Name of table
    __tablename__ = 'merchandise_items'
    id = Column(Integer, primary_key = True)
    item_name = Column(String(50), index = True)

    sales_of_items = relationship('SalesOfItems', back_populates = 'merchandise_items')
    dates_games = relationship('DatesOfGames', back_populates = 'merchandise_items')

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
    merchandise_items = relationship('MerchandiseItems', back_populates = 'sales_of_items')

    dates_games = relationship('DatesOfGames', back_populates = 'sales_of_items')

    def __repr__(self):
        return 'Item sold id: {:<2} quantity sold = {:<10} price each = {:>5} \
                total sale = ${:>5} item id = {}'\
                .format(self.id, self.merchandise_items, self.price_per_unit, \
                self.total_price, self.items_id, self.merchandise_items) #self.merchandise_items, self.sales_of_items)


class DatesOfGames(Base):
    ''' This will store hte game's dates table'''
    __tablename__ = 'dates_games'
    # Add columns
    id = Column(Integer, primary_key = True)
    date_of_game = Column(String(20), nullable = False) # Format mm/dd/yyyy
    city = Column(String(50), nullable = False)
    state = Column(String(50), nullable = False)

    sales_id = Column(Integer, ForeignKey('sales_of_items.id'))
    sales_of_items = relationship('SalesOfItems', back_populates = 'dates_games')

    item_name_id = Column(Integer, ForeignKey('merchandise_items.id'))
    merchandise_items = relationship('MerchandiseItems', back_populates = 'dates_games')


    # sales_of_items = relationship('SalesOfItems', back_populates = 'dates_games')
    def __repr__(self):
        return ' ID = {:}  Date = {:<11} City = {:<12} State = {} Sales ID = {} Item_name ID {}'\
        .format(self.id, self.date_of_game, self.city.capitalize(), \
        self.state, self.sales_id, self.item_name_id, self.sales_of_items, self.merchandise_items)



Base.metadata.create_all(engine)




# time_created = Column(DateTime(timezone=True), server_default=func.now())
# time_updated = Column(DateTime(timezone=True), onupdate=func.now())
# from datetime import datetime
# dt = datetime(2001, 2, 3, 4, 5)
# New
#
# '{:{dfmt} {tfmt}}'.format(dt, dfmt='%Y-%m-%d', tfmt='%H:%M')
# Output
#
# 2001-02-03 04:05
