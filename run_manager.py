
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# Import tables and classes
from tables_setUp import MerchandiseItems, DatesOfGames, SalesOfItems
from add_items import Add_items_to_tables
import queries_functions

Session = sessionmaker(bind = engine)

def main():
    print('##### WELCOME TO THE MERCHANDISE SALES APP #######')

    MerchandiseItems() # the MerchandiseItems table is loaded
    DatesOfGames() # Load the date of games table
    SalesOfItems() # Loas the sales table

    Add_items_to_tables.add_merch_items()
    Add_items_to_tables.add_dates_cities()

    queries_functions.get_all_fromTable(MerchandiseItems)
    Add_items_to_tables.sold_items()

    print()
    print('\n   This is the list of all the items sold1')
    queries_functions.get_all_fromTable(SalesOfItems)
    print()

    print('\n#This are the total items sold by each date!')
    queries_functions.get_sum_sold_items()
    Session().close()


if __name__ == '__main__':
    while True:
        main()
        resp = input('Do you want to continue? Y/N: ')
        if resp == 'n'.lower():
            break
