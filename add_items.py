''' This class is to add data to tables'''
from sqlalchemy.orm import sessionmaker
from tables_setUp import MerchandiseItems, DatesOfGames, SalesOfItems
# from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, func, funcfilter
import time


# This is to save data to tables
engine = create_engine('sqlite:///merchandise_sales.db', echo=False)
Session = sessionmaker(bind=engine) # Helps set up the database.


save_inputs = Session() # This variable is used to add items on all tables.
class Add_items_to_tables():

        # This function is set up incase the user ones to add a new brand
    def add_merch_items():
        ''' This is for the names, and it loads some of the items for the user.
        If the user wants to add another name, there is an option available'''
        # # This creates the initial names that will be stored in the database.
        # Add the initial items.

        # Here I am using a function named count_rows check if table is empty.
        if Add_items_to_tables.count_rows(MerchandiseItems): # If not items found when the app first runs
            save_inputs.bulk_insert_mappings(MerchandiseItems,\
                                    [dict(item_name = 'Jerseys'),\
                                    dict(item_name = 'Hats'),\
                                    dict(item_name = 'Dvds')])
            save_inputs.commit()
            # Using bulk_insert

        # If the user wants to add a new brand
        print('\nThis is the list of merchandise items')
        for name in save_inputs.query(MerchandiseItems): # Prints the list of the names
            print(name)
        while True:
            add_more = input('\nDo you want to add a new name to the list? Y/N:\n')
            if add_more == 'n'.lower():
                break
            else:
                # This code will veryfy that the user does not enter a repeated name.
                new_item_name = input("Enter the new name: ")
                exists = save_inputs.query(save_inputs.query(MerchandiseItems) \
                      .filter_by(item_name = new_item_name) \
                      .exists()).scalar()
                if exists:
                    print('Name already in list!')
                else:
                    add_new_name = MerchandiseItems(item_name = new_item_name)
                    save_inputs.add_all([add_new_name])
                    save_inputs.commit()
                    print(new_item_name, ' was added to merchandises table in DB')
                    break




    def add_dates_cities():
        ''' This adds dates and cities to the table dates of games.'''
        # Here I am using a function named count_rows check if table is empty.
        if Add_items_to_tables.count_rows(DatesOfGames): # If not items found when the app first runs
            save_inputs.bulk_insert_mappings(DatesOfGames,\
                    [dict(date_of_game = '02/15/2017', city = 'Burnsville', state = 'MN'),\
                     dict(date_of_game = '02/20/2017', city = 'Minneapolis', state = 'MN'),\
                     dict(date_of_game = '03/20/2017', city = 'Lakeville', state = 'MN'),\
                     dict(date_of_game = '03/25/2017', city = 'Edina', state = 'MN')])
            save_inputs.commit()
            # Using bulk_insert

            # This is for the user to enter new dates.
        # while True:
        #     user_response = input('\nDo you want to add more dates, cities? Y/N: ')
        #     if user_response == 'n':
        #         break
        #     else:
        #         date = Add_items_to_tables.date_validation()
        #         city = input('Enter the name of the city:\n')
        #         state = input('Enter the state like (MN):\n')
        #         new_date = DatesOfGames(date_of_game = date, city = city, state= state)
        #         save_inputs.add_all([new_date])
        #         save_inputs.commit()


    save_inputs.close()
    Session.close_all()


        # format Date to make sure user enter the right format.
    def date_validation():
        ''' This validates the date that the user entered. '''
        while True:
            date = input('Enter the date (mm/dd/yyy):\n')
            try:
                # This formats the Date.
                valid_date = time.strptime(date, '%m/%d/%Y')
                if valid_date: # If Date is formatted correctly, loop breaks
                    break
            except:
                print('Invalid data!')
                continue
        return date

    # This is to check if the table has any data or rows in it.
    def count_rows(table):
        zero_rows = True
        rows_count = save_inputs.query(table).count()
        if rows_count == 0:
            return zero_rows
        else:
            return zero_rows == False
