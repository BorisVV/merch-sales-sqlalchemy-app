
from flask import \
        render_template, redirect, url_for, abort, request, flash

from app_sport_team import app
from app_sport_team.tables_setUp import \
            db_session, MerchandiseItems, SalesOfItems, DatesOfGames

# Query all the merchandise items.
def items_query(): # TODO:  find a better way to do it?
    return MerchandiseItems.query.all()

# Query all the game's dates.
def dates_query(): # TODO:  find a better way to do it?
    return DatesOfGames.query.all()

# For example purpose, this is the first pages displayed.
@app.route('/')
def base(): # TODO: remove in future.
    return render_template('base.html')

# This page will display the table for the items and options for others pages.
@app.route('/home/')
def home():
    items = items_query()
    return render_template('home.html', items=items)

# :flash: In the base.html there is a block inside the body block that exexutes
# the messsages. uses the syntax (var = get_flashed_messages()) and
# will display messages for users to read and correct inputs, etc.

# User can enter new items, form is displayed.
@app.route('/add_items/', methods=['GET', 'POST'])
def addItems():
    items = items_query()
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

# TODO: add option to add the id #/<int:id>/ or item being modified on the url.

@app.route('/edit_items/', methods=['GET', 'POST'])
def editItems():
    items = items_query()
    if request.method == 'POST':
        # Query to get the item's name with the selected id from the form.
        items_row = MerchandiseItems.query.get(request.form['_item_id'])
        # item_id = request.form['_item_id'] # gets the id number only.

        if 'delete' in request.form:
            # name = items_row.name
            db_session.delete(items_row)
            db_session.commit()
            flash(u'%r was deleted <br> Do you want to delete/update more.\
                    <br>"Cancel" to quit' % items_row.name)
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
                        % (old_name, new_name))
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
    # Enter new dates for games.
    _dates = dates_query()

    form = dict(game_date=_dates.game_date, )

    if request.method == 'POST':
        date_game = request.form['date_game']
        city = request.form['city']
        state = request.form['state']

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        else:
            for _date in _dates:
                if _date.game_date == date_game:
                    flash(u'Date {} is already in file it can\'t be used twice!'.format(date_game))
                    return render_template('addDates.html',\
                        date_game=date_game, city=city, state=state)

            if date_game == '' or city == '' or state == '':
                flash('No blank text boxes allowed!')
                return render_template('addDates.html', date_game=date_game, \
                                city=city, state=state)

            db_session.add(DatesOfGames(game_date=str(date_game), city=city, state=state))
            db_session.commit()
            flash('Success! <br> Date: {}, City: {}, State: {}, was added to\
                    <br> Games\'s Schedules <br> Would you like to add more?\
                    \'Cancel\' to exit'.format(date_game, city, state))
            return redirect(url_for('addDates'))

    return render_template('addDates.html', _dates=_dates)

@app.route('/show_dates/')
def show_dates():
    _dates = dates_query()
    return render_template('show_dates.html', _dates=_dates)

@app.route('/edit_sold_items/', methods=['GET', 'POST'])
def updateSoldItems():
    items = items_query()
    _dates = dates_query()

    if request.method == 'POST':

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        item_id = int(request.form['selected_item'])
        date_id = int(request.form['selected_date'])
        # name = MerchandiseItems.query.get(request.form['selected_item'])
        # _date = DatesOfGames.query.get(request.form['selected_date'])
        qty = request.form['quantity']
        price = request.form['price']
        try:
            price = float(price)
            if price < 0 or price > 150:
                flash(u'Make sure the price is between 0(zero) and 150.\
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
            flash(u'Check price and make sure is a number. <br>\
                    You entered %r' % price)
            return render_template('updateSoldItems.html',\
                    items=items, _dates=_dates, item_id=item_id, \
                    date_id=date_id, qty=qty, price='')

    return render_template('updateSoldItems.html', items=items, _dates=_dates)

@app.route('/display_redords/')
def displaySoldRecords():
    itemsSold = SalesOfItems.query.all()
    return render_template('displaySoldRecords.html', itemsSold=itemsSold)
