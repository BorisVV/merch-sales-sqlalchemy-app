
from datetime import datetime
from flask import \
        render_template, redirect, url_for, abort, request, flash

from app_sport_team import app
from app_sport_team.tables_setUp import \
            db_session, MerchandiseItems, SalesOfItems, DatesOfGames
from app_sport_team import utils

# For example purpose, this is the first pages displayed.
# :flash: In the base.html there is a block inside the body block that exexutes
# the messsages. uses the syntax (var = get_flashed_messages()) and
# will display messages for users to read and correct inputs, etc.
@app.route('/')
def index(): # TODO: remove in future.
    return render_template('index.html')

# User can enter new items, form is displayed.
@app.route('/add_items/', methods=['GET', 'POST'])
def addItems():
    items = MerchandiseItems.query.all()
    if request.method == 'POST':

        if 'cancel' in request.form:
            flash('The option to add items was canceled!')
            return redirect(url_for('displaySoldRecords'))

        else:
            # Save button was clicked.
            # str.capitalize()
            new_name = request.form['name'].capitalize()

            if new_name == "":  # validate input.
                flash('Oops! It cannot be blank')
                return redirect(url_for('addItems'))

            for name in items:
                if  name.name == new_name: # if name already in table.
                    flash('Name %r already exist. <br>Try a different one' % new_name)
                    return redirect(url_for('addItems'))

            # The new name will be add if passed the above stataments.
            db_session.add(MerchandiseItems(name=new_name))
            db_session.commit()
            flash('Success! %r was added.' % new_name + '<br>Do you want ' \
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
            flash('%r was deleted <br> Do you want to delete/update more.\
                    <br>"Cancel" to quit.' % name)
            return render_template('editItems.html', items=items)

        elif 'update' in request.form:
            new_name = request.form['new_name']
            if new_name == "":
                flash('Text box cannot be blank, name required! <br> \
                        Enter new  name for the selected name! --> ' + items_row.name)
                return render_template('editItems.html', items=items, item_id=items_row.id)

            try:
                old_name = items_row.name # Stored to display old name.
                items_row.name = new_name.capitalize() # Change the name.
                db_session.commit()
                # Display message.
                flash('%r was updated succesfully! with --> %r' \
                        % (old_name, items_row.name))
                flash('delete/update another? "Cancel" to quit')
                # Render the template again with the updated item selected.
                return render_template('editItems.html', items=items, item_id=items_row.id)
            except:
                db_session.rollback() # If not Exception will raise.
                flash('%r is already in file, try a different name' % new_name)
                # Re-render the template with the users inputs.
                return render_template('editItems.html', items=items, item_id=items_row.id, new_name=new_name)

        else: # If cancel button is clicked.
            return redirect(url_for('index'))

    return render_template('editItems.html', items=items)

@app.route('/add_dates/', methods=['GET', 'POST'])
def addDates():
    # Collect the date, city and state for the game.
    if request.method == 'POST':
        date_game = request.form['date_game']
        city = request.form['city']
        state = request.form['state']

        if 'cancel' in request.form:
            flash('The add dates option was canceled!')
            return redirect(url_for('displaySoldRecords'))

        else:
            # This is to make sure that boxes are not empty.
            if date_game == '' or city == '' or state == '':
                flash('No blank text boxes allowed!')
                return render_template('addDates.html', date_game=date_game, \
                city=city, state=state)

            # Need to validate the input and make sure that date in not
            # already in db.
            try:
                dt = utils.format_date(date_game)
                db_session.add(DatesOfGames(game_date=dt, city=city, state=state))
                db_session.commit()
                flash('Success! <br> \
                Date: {}, City: {}, State: {} <br> \
                was added to Games\' Schedules <br>  \
                Would you like to add more? \'Cancel\' to exit.' \
                .format(date_game, city, state)
                )
                return redirect(url_for('addDates'))
            except Exception as e:
                db_session.rollback() # TODO overdoing?
                flash('Date {} is already in file it can\'t be used twice!'.format(date_game))
                flash('Or this happened ' + str(e))
                return render_template('addDates.html',\
                    date_game=date_game, city=city, state=state)

    return render_template('addDates.html')

@app.route('/display_games_sched/')
def displayGameSched():
    return render_template('displayGameSched.html', _dates=DatesOfGames.query.all())

@app.route('/edit_schedules/<int:id>/', methods=['GET', 'POST'])
def editDates(id):
    sched = DatesOfGames.query.get(id)
    # Date is in the form Y-m-d @ m:s:.etc which is bad for
    # reding, the strftime solves that problem.
    dt = datetime.strftime(sched.game_date, '%Y-%m-%d')
    # This is to display the deleted information.
    dt_str = tuple((dt, str(sched.city), str(sched.state)))

    form = dict(_date="", city="", state="")
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('displayGameSched'))

        # Format date to convert it to sqlalchey DateTime
        form['_date'] = utils.format_date(request.form['date'])
        form['city'] = request.form['city']
        form['state'] = request.form['state']
        # If the boxes are left blank.
        if form['_date'] == "":
            form['_date'] = sched.game_date
        if form['city'] == "":
            form['city'] = sched.city
        if form['state'] == "":
            form['state'] = sched.state

        # Assuming that nothing goes wrong.
        if 'delete' in request.form:
            db_session.delete(sched)
            db_session.commit()
            flash('Deleted ' + str(dt_str))
            return redirect(url_for('displayGameSched'))

        else:
            try:
                # Update the data.
                sched.game_date = form['_date']
                sched.city = form['city']
                sched.state = form['state']
                db_session.commit()
                flash('Updated succesfully!')
                return redirect(url_for('displayGameSched'))
            except:
                flash('Something went wrong')
                return redirect(url_for('editDates'))
    return render_template('editDates.html', form=form, sched=sched)

@app.route('/add_sold_records/', methods=['GET', 'POST'])
def addSoldRecord():
    items = MerchandiseItems.query.all()
    _dates = DatesOfGames.query.all()

    # TODO:  Create a form dict for render_template.

    if request.method == 'POST':

        if 'cancel' in request.form:
            return redirect(url_for('displaySoldRecords'))

        else:
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
                    flash('Make sure the price is between 1.00 and 150.00.\
                        <br>You entered %r' % price)
                    return render_template('addSoldRecord.html',\
                            items=items, _dates=_dates, item_id=item_id, \
                            date_id=date_id, qty=qty, price='')
                else:
                    db_session.add(SalesOfItems(item_id=item_id, _date_id=date_id, quantity_sold=qty, price_per_unit=price))
                    db_session.commit()
                    flash('Record added and saved succesfully!')
                    return redirect(url_for('displaySoldRecords'))
            except:
                # The input was a string not a numeric value.
                flash('Check price and make sure is a number. <br>\
                        You entered %r' % price)
                return render_template('addSoldRecord.html',\
                        items=items, _dates=_dates, item_id=item_id, \
                        date_id=date_id, qty=qty, price=price)

    return render_template('addSoldRecord.html', items=items, _dates=_dates)

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

    form = dict(qty=modifySold.quantity_sold, \
                price=modifySold.price_per_unit, \
                name=modifySold.merchandise_items.name, \
                _date=modifySold.games_schedules.game_date
                )
    if request.method == 'POST':

        if 'cancel' in request.form:
            flash('Transaction canceled!')
            return redirect(url_for('displaySoldRecords'))

        elif 'delete' in request.form:
            db_session.delete(modifySold)
            db_session.commit()
            flash('Record deleted!')
            return redirect(url_for('displaySoldRecords'))

        else:
            form['qty'] = request.form['quantity']
            form['price'] = request.form['price']

            # The table takes a float for price, try/except is very handy here.
            try:
                new_price = float(form['price'])
                modifySold.quantity_sold = form['qty']
                modifySold.price_per_unit = new_price
                db_session.commit()
                flash('Success, data updated!!')
            except Exception as e:
                db_session.rollback()
                flash('Error, ' + str(e))

    return render_template('editSoldRecords.html', form=form, \
                            modifySold=modifySold)
