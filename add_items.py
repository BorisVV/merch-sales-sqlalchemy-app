''' This class is to add data to tables'''
from sqlalchemy.orm import sessionmaker
from tables_setUp import MerchandiseItems, DatesOfGames, SalesOfItems
# from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
import time

# This is to save data to tables
engine = create_engine('sqlite:///merchandise_sales.db', echo=False)
Session = sessionmaker(bind=engine) # Helps set up the database.


save_inputs = Session() # This variable is used to add items on all tables.
class Add_items_to_tables():

        # This function is set up incase the user ones to add a new brand
    def add_merch_items():
        ''' This is for the names, and it loads some of the items
        for the user. If the user wants to add another brand this
        option is available'''
        # # This creates the initial names that will be stored in the database.
        ''' Uncomment this block of code to add item names manualy'''
        # jerseys = MerchandiseItems(item_name = 'Jerseys')
        # hats = MerchandiseItems(item_name = 'Hats')
        # dvds = MerchandiseItems(item_name = 'Dvds') # games of team
        # save_inputs.add_all([jerseys, hats, dvds])
        # save_inputs.commit()

        # If the user wants to add a new brand
        print('\nThis is the list of merchandise items')
        for name in save_inputs.query(MerchandiseItems): # Prints the list of the names
            print(name)
        while True:
            add_more = input('Do you want to add another name? Y/N: ')
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
        while True:
            date = Add_items_to_tables.date_validation()
            city = input('Enter the name of the city: ')
            new_date = DatesOfGames(date_of_game = date, city = city)
            save_inputs.add_all([new_date])
            save_inputs.commit()
            user_response = input('Do you want to add more dates, cities? Y/N: ')
            if user_response == 'n':
                break


    save_inputs.close()
    Session.close_all()

        # format Date.
    def date_validation():
        ''' This validates the date that the user entered. '''
        while True:
            date = input('Enter the date (mm/dd/yyy): ')
            try:
                # This formats the Date.
                valid_date = time.strptime(date, '%m/%d/%Y')
                if valid_date: # If Date is formatted correctly, loop breaks
                    break
            except:
                print('Invalid data!')
                continue
        return date
