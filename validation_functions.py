

import time




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


# Validates numeric values.
def numeric_validation(message):
    while True:
        if message.isnumeric():
            break
        else:
            print(input('Not a valid number, enter it again:\n'))
