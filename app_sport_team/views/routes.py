
from flask import \
        render_template, redirect, url_for, abort, request, flash

from app_sport_team import app
from app_sport_team.tables_setUp import \
            db_session, MerchandiseItems, SalesOfItems, DatesOfGames

# For example purpose, this is the first pages displayed.
@app.route('/')
def base(): # TODO: remove in future.
    return render_template('base.html')

# This page will display the table for the items and options for others pages.
@app.route('/home/')
def home():
    return render_template('home.html', items=MerchandiseItems.query.all())

# :flash: In the base.html there is a block inside the body block that exexutes
# the messsages. uses the syntax (var = get_flashed_messages()) and
# will display messages for users to read and correct inputs, etc.

# User can enter new items, form is displayed.
@app.route('/add_items/', methods=['GET', 'POST'])
def addItems():
    items = MerchandiseItems.query.all()
    if request.method == 'POST':

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        else:
            # Save button was clicked.
            # str.capitalize()
            new_name = request.form['name'].capitalize()

            if new_name == "":  # validate input.
                flash(u'Oops! It cannot be blank')
                return redirect(url_for('addItems'))

            for name in items:
                if  name.name == new_name: # if name already in table.
                    flash(u'Name %r already exist. <br>Try a different one' % new_name)
                    return redirect(url_for('addItems'))

            # The new name will be add if passed the above stataments.
            db_session.add(MerchandiseItems(name=new_name))
            db_session.commit()
            flash(u'Success! %r was added.' % new_name + u'<br>Do you want ' \
                    'to add another one? "Cancel to exit"')
            return redirect(url_for('addItems')) # option to add more.

    return render_template('addItems.html', items=items)

@app.route('/edit_items/', methods=['GET', 'POST'])
def editItems():
    # TODO: add option to add the id #/<int:id>/ or item being modified on the url.
    items = MerchandiseItems.query.all()
    if request.method == 'POST':
        # Query to get the item's name with the selected id from the form.
        items_row = MerchandiseItems.query.get(request.form['_item_id'])
        # item_id = request.form['_item_id'] # gets the id number only.

        if 'delete' in request.form:
            name = items_row.name # Store old name.
            db_session.delete(items_row)
            db_session.commit()
            flash(u'%r was deleted <br> Do you want to delete/update more.\
                    <br>"Cancel" to quit.' % name)
            return render_template('editItems.html', items=items)

        elif 'update' in request.form:
            new_name = request.form['new_name']
            if new_name == "":
                flash(u'Text box cannot be blank, name required! <br> \
                        Enter new  name for the selected name! --> ' + items_row.name)
                return render_template('editItems.html', items=items, item_id=items_row.id)

            try:
                old_name = items_row.name # Stored to display old name.
                items_row.name = new_name.capitalize() # Change the name.
                db_session.commit()
                # Display message.
                flash(u'%r was updated succesfully! with --> %r' \
                        % (old_name, items_row.name))
                flash(u'delete/update another? "Cancel" to quit')
                # Render the template again with the updated item selected.
                return render_template('editItems.html', items=items, item_id=items_row.id)
            except:
                db_session.rollback() # If not Exception will raise.
                flash('%r is already in file, try a different name' % new_name)
                # Re-render the template with the users inputs.
                return render_template('editItems.html', items=items, item_id=items_row.id, new_name=new_name)

        else: # If cancel button is clicked.
            return redirect(url_for('home'))

    return render_template('editItems.html', items=items)

@app.route('/add_dates/', methods=['GET', 'POST'])
def addDates():
    _dates = DatesOfGames.query.all()
    # Collect the date, city and state for the game.
    if request.method == 'POST':
        date_game = request.form['date_game']
        city = request.form['city']
        state = request.form['state']

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        else:
            # Need to validate the input and make sure that date in not
            # already in db.
            if date_game != "":
                for _date in _dates:
                    if _date.game_date == date_game:
                        flash(u'Date {} is already in file it can\'t be used twice!'.format(date_game))
                        return render_template('addDates.html',\
                            date_game=date_game, city=city, state=state)

            # This is to make sure that boxes are not empty.
            elif date_game == '' or city == '' or state == '':
                flash('No blank text boxes allowed!')
                return render_template('addDates.html', date_game=date_game, \
                city=city, state=state)

            db_session.add(DatesOfGames(game_date=str(date_game), city=city, state=state))
            db_session.commit()
            flash('Success! <br> \
            Date: {}, City: {}, State: {} <br> \
            was added to Games\' Schedules <br>  \
            Would you like to add more? \'Cancel\' to exit.' \
            .format(date_game, city, state)
            )
            return redirect(url_for('addDates'))

    return render_template('addDates.html', _dates=_dates)

@app.route('/show_dates/')
def show_dates():
    return render_template('show_dates.html', _dates=DatesOfGames.query.all())

@app.route('/edit_sold_items/', methods=['GET', 'POST'])
def updateSoldItems():
    items = MerchandiseItems.query.all()
    _dates = DatesOfGames.query.all()

    if request.method == 'POST':

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        # In the html there is a select and options. The values/id are
        # collected from the select for both item and date.
        item_id = int(request.form['selected_item'])
        date_id = int(request.form['selected_date'])

        # This two lines below are for example only.
        # name = MerchandiseItems.query.get(request.form['selected_item'])
        # _date = DatesOfGames.query.get(request.form['selected_date'])

        # The input has the values for qty and price.
        qty = request.form['quantity']
        price = request.form['price']

        # The price is a string and needs to be converted to float and if
        # the input is not a number it will raise an Exception.
        try:
            price = float(price)

            # for small example we need to keep data small.
            if price < 1 or price > 150:
                flash(u'Make sure the price is between 1.00 and 150.00.\
                    <br>You entered %r' % price)
                return render_template('updateSoldItems.html',\
                        items=items, _dates=_dates, item_id=item_id, \
                        date_id=date_id, qty=qty, price='')
            else:
                db_session.add(SalesOfItems(item_id=item_id, _date_id=date_id, quantity_sold=qty, price_per_unit=price))
                db_session.commit()
                flash(u'Record updated succesfully! <br>'\
                        'Do you want to updated more? \'Cancel\' to quit!')
                return render_template('updateSoldItems.html', items=items, _dates=_dates)

        except:
            # The input was a string not a numeric value.
            flash(u'Check price and make sure is a number. <br>\
                    You entered %r' % price)
            return render_template('updateSoldItems.html',\
                    items=items, _dates=_dates, item_id=item_id, \
                    date_id=date_id, qty=qty, price=price)

    return render_template('updateSoldItems.html', items=items, _dates=_dates)

@app.route('/display_redords/')
def displaySoldRecords():
    return render_template('displaySoldRecords.html', itemsSold=SalesOfItems.query.all())

@app.route('/edit_sold_records/<int:id>/', methods=['GET', 'POST'])
def editSoldRecords(id):
    # id is from the displaySoldRecords.html
    modifySold = SalesOfItems.query.get(id)

    if modifySold is None:
        flash('Issues with id...')
        return redirect(url_for('displaySoldRecords'))
    if request.method == 'POST':
        if 'cancel' in request.form:
            flash(u'Transaction canceled!')
            return redirect(url_for('displaySoldRecords'))

    return render_template('editSoldRecords.html', modifySold=modifySold)
