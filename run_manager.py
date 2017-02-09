

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Import tables and classes
from tables_setUp import MerchandiseItems, DatesOfGames, SalesOfItems
from add_items import Add_items_to_tables
import queries_functions

all_rows = queries_functions


engine = create_engine('sqlite:///merchandise_sales.db', echo=False)
Session = sessionmaker(bind = engine)

print('\n\n##### WELCOME TO THE MERCHANDISE DATABASE #######\n')

def main():
    MerchandiseItems() # the MerchandiseItems table is loaded
    DatesOfGames() # Load the date of games table
    SalesOfItems() # Loas the sales table

    # Add_items_to_tables.add_merch_items()
    # Add_items_to_tables.add_dates_cities()
    #
    # all_rows.get_all_fromTable(MerchandiseItems)
    # Add_items_to_tables.sold_items()

    print()
    all_rows.get_all_fromTable(SalesOfItems)


    Session().close()


if __name__ == '__main__':
    main()
