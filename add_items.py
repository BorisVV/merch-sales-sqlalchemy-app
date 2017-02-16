''' This class is to add data to tables'''
from sqlalchemy.orm import sessionmaker
from tables_setUp import MerchandiseItems, DatesOfGames, SalesOfItems
# from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, func, funcfilter
import time
import queries_functions
import validation_functions
from eng_sess_base_setUP import E_S_B

# This is to save data to tables
engine = E_S_B.engine
Session = E_S_B.Session



save_inputs = Session() # This variable is used to add items on all tables.

class Add_items_to_tables():

        # This function is set up incase the user ones to add a new brand
    def add_merch_items():
        ''' This is for the names, and it loads some of the items for the user.
        If the user wants to add another name, there is an option available'''
        # # This creates the initial names that will be stored in the database.
        # Add the initial items.

        # Here I am using a function named count_rows check if table is empty.
        if queries_functions.count_rows(MerchandiseItems): # If not items found when the app first runs
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
            add_more = input('*Do you want to add a new name to the list? Y/N:\n')
            if add_more == 'n'.lower():
                break
            else:
                # This code will veryfy that the user does not enter a repeated name.
                new_item_name = input('-->Enter the new name: ')
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
        if queries_functions.count_rows(DatesOfGames): # If not items found when the app first runs
            save_inputs.bulk_insert_mappings(DatesOfGames,\
                    [dict(date_of_game = '02/15/2017', city = 'Burnsville', state = 'MN'),\
                     dict(date_of_game = '02/20/2017', city = 'Minneapolis', state = 'MN'),\
                     dict(date_of_game = '03/20/2017', city = 'Lakeville', state = 'MN'),\
                     dict(date_of_game = '03/25/2017', city = 'Edina', state = 'MN')])
            save_inputs.commit()
            # Using bulk_insert

            # This is for the user to enter new dates.
    def add_more_Dates():
        while True:
            user_response = input('*Do you want to add different date, city and state? Y/N:\n')
            if user_response == 'n'.lower():
                break
            else:
                date = validation_functions.date_validation()
                exists = save_inputs.query(save_inputs.query(DatesOfGames) \
                      .filter_by(date_of_game = date) \
                      .exists()).scalar()
                if exists:
                    print('**Warning! \nDate was not added because is already in the list!**')
                else:
                    city = input('-->Enter the name of the city:\n')
                    state = input('-->Enter the state like (MN):\n')
                    new_date = DatesOfGames(date_of_game = date, city = city, state= state)
                    save_inputs.add_all([new_date])
                    save_inputs.commit()


    def sold_items():
        ''' This function is to save the items sold for each game '''

        print('\n          Here is the list of games')
        queries_functions.get_all_fromTable(DatesOfGames) # Prints the games table
        Add_items_to_tables.add_more_Dates() # Let's the user decide if it wants to add more

        while True:
            resp = input('*Do you want to add more sold items for a specific date? Y/N: ')
            if resp == 'n'.lower():
                break
            else:
                print('\nLet\'s add some sold item to one of the games on a specific Date \nSelect the "ID" from one of the dates above.')
                date_id = int(input('-->Enter the ID number:\n'))
                queries_functions.get_all_fromTable(MerchandiseItems)
                item_id = int(input('-->Enter the ID from the items above:\n'))
                quantity_sold = int(input('-->Enter total quantity sold:\n'))
                price_unit = float(input('-->Enter the price per unit:\n'))
                total = float(quantity_sold * price_unit)

                new_sold_item = SalesOfItems(quantity_sold = quantity_sold, \
                    price_per_unit = price_unit, total_price = total, \
                    items_id = item_id, dates_id = date_id)

                save_inputs.add_all([new_sold_item])
                save_inputs.commit()




    save_inputs.close()
    Session.close_all()
