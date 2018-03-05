
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
            return redirect(url_for('index'))

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
            flash('Success! "{}" was added.'.format(new_name) + '<br>Do you want ' \
                    'to add another one? "Cancel to exit"')
            return redirect(url_for('addItems')) # option to add more.

    return render_template('addItems.html', items=items)

@app.route('/display_items/')
def displayItems():
    items=MerchandiseItems.query.all()
    if not items:
        flash('There are not items in db. Add some first.')
        return redirect(url_for('addItems'))
    return render_template('displayItems.html', items=items)

@app.route('/edit_items/', methods=['GET', 'POST'])
def editItems():
    # TODO: add option to add the id #/<int:id>/ or item being modified on the url.
    items = MerchandiseItems.query.all()
    if request.method == 'POST':
        # Query to get the item's name with the selected id from the form.
        item_row = MerchandiseItems.query.get(request.form['item_selected'])
        # item_id = request.form['item_selected'] # gets the id number only.

        if 'delete' in request.form:
            name = item_row.name # Store old name.
            db_session.delete(item_row)
            db_session.commit()
            flash('{} was deleted <br> Do you want to delete/update more.\
                    <br>"Cancel" to quit.'.format(name))
            return render_template('editItems.html', items=MerchandiseItems.query.all())

        elif 'update' in request.form:
            new_name = request.form['new_name']
            if new_name == "":
                flash('Text box cannot be blank, name required! <br> \
                        Enter new  name for the selected name! --> ' + item_row.name)
                return render_template('editItems.html', items=items, item_id=item_row.id)

            try:
                old_name = item_row.name # Stored to display old name.
                item_row.name = new_name.capitalize() # Change the name.
                db_session.commit()
                # Display message.
                flash('"{}" was updated succesfully! with --> "{}"' \
                        .format(old_name, item_row.name))
                flash('delete/update another? "Cancel" to quit')
                # Render the template again with the updated item selected.
                return render_template('editItems.html', items=items, item_id=item_row.id)
            except:
                db_session.rollback() # If not Exception will raise.
                flash('%r is already in file, try a different name' % new_name)
                # Re-render the template with the users inputs.
                return render_template('editItems.html', items=items, item_id=item_row.id, new_name=new_name)

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
            return redirect(url_for('index'))

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
                db_session.add(DatesOfGames(game_date=dt, city=city, state=state.upper()))
                db_session.commit()
                flash('Success! <br> \
                Date: {}, City: {}, State: {} <br> \
                was added to Games\' Schedules <br>  \
                Would you like to add more? \'Cancel\' to exit.' \
                .format(date_game, city, state)
                )
                return redirect(url_for('addDates'))
            except:
                db_session.rollback()
                flash('Date {} is already in file it can\'t be used twice!'.format(date_game))

                return render_template('addDates.html',\
                    date_game=date_game, city=city, state=state)

    return render_template('addDates.html')

@app.route('/display_games_sched/')
def displayGameSched():
    _dates=DatesOfGames.query.all()
    if not _dates:
        flash('There are not dates in db. Add some first.')
        return redirect(url_for('addDates'))
    return render_template('displayGameSched.html', _dates=_dates)

@app.route('/edit_schedules/<int:id>/', methods=['GET', 'POST'])
def editDates(id):
    sched = DatesOfGames.query.get(id)
    dates_in_soldRecords = SalesOfItems.query.filter_by(date_id=id).all()

     # category = Category.query.filter_by(slug=slug).first()
     # snippets = category.snippets.order_by(Snippet.title).all()

    # Date is in the form Y-m-d @ m:s:.etc which is bad for
    # reding, the strftime solves that problem.
    dt = datetime.strftime(sched.game_date, '%Y-%m-%d')

    # This is to display the deleted information.
    dt_str = tuple((dt, str(sched.city), str(sched.state)))

    form = dict(_date=sched.game_date, city=sched.city, state=sched.state)
    if request.method == 'POST':

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

        if 'cancel' in request.form:
            return redirect(url_for('index'))

        # Assuming that nothing goes wrong.
        elif 'delete' in request.form:
            db_session.delete(sched)
            for record in dates_in_soldRecords:
                db_session.delete(record)
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
    soldRec = SalesOfItems.query.all()

    # We need to verify that there are records in db. first.
    if not items:
        flash('Warning!!! <br> There not items in db, you first need to add items.<br>' \
                'Then you can add Sold Records.')
        return redirect(url_for('addItems'))
    if not _dates:
        flash('Warning!!! <br> There not dates in db, you first need to add dates.<br>' \
                'Then you can add Sold Records.')
        return redirect(url_for('addDates'))


    # TODO:  Create a form dict for render_template.

    if request.method == 'POST':

        if 'cancel' in request.form:
            flash('Transaction canceled!')
            return redirect(url_for('displaySoldRecords'))

        else: # Save was clicked.
            # In the html there is a select and options. The values/id are
            # collected from the select for both item and date.

            # This two lines below are for example only/ both get the full row
            # name_row = MerchandiseItems.query.get(request.form['selected_item'])
            # _date_row = DatesOfGames.query.get(request.form['selected_date'])

            date_id = int(request.form['selected_date'])
            item_id = int(request.form['selected_item'])
            # For qty the box is a numeric type so theres no need to convert it.
            qty = request.form['quantity']
            # For price the box is a text type and needs to be converted to float.
            price = request.form['price']

            for row in soldRec:
                if date_id == row._date_id and item_id == row.item_id:
                    _date = str(row.games_schedules.game_date).replace('00:00:00', ' ')
                    flash('Warning!!! <br> Transaction canceled!')
                    flash('Name= {} and Date= {} is already in file. <br> \
                           Go to link above "sold records" to edit the record.' \
                    .format(row.merchandise_items.name, _date))

                    return render_template('addSoldRecord.html',\
                                    items=items, _dates=_dates, item_id=item_id, \
                                    date_id=date_id, qty=qty, price=price)

            try:
                price = float(price)
                # for small example we need to keep numbers small.
                if price < 0 or price > 150:
                    flash('Make sure the price is between 0.00 and 150.00.\
                    <br>You entered %r' % price)
                    return render_template('addSoldRecord.html',\
                    items=items, _dates=_dates, item_id=item_id, \
                    date_id=date_id, qty=qty, price='')
            except:
                # The input was a string not a numeric value.
                flash('Check box price and make sure is a numeric value. <br>\
                        You entered {}'.format(price))
                return render_template('addSoldRecord.html',\
                                    items=items, _dates=_dates, item_id=item_id, \
                                    date_id=date_id, qty=qty, price=price)

            # If not nothing fails above.
            db_session.add(SalesOfItems(item_id=item_id, _date_id=date_id, quantity_sold=qty, price_per_unit=price))
            db_session.commit()
            flash('Record added and saved succesfully! <br> Add more?')
            return render_template('addSoldRecord.html', date_id=date_id, item_id=item_id, price=price, qty=qty, _dates=_dates, items=items)

    return render_template('addSoldRecord.html', items=items, _dates=_dates)

@app.route('/display_redords/')
def displaySoldRecords():
    itemsSold = SalesOfItems.query.order_by(SalesOfItems._date_id).all()
    if not itemsSold:
        flash('Warning!!! <br> There are not sold records in db. Add some first!')
    return render_template('displaySoldRecords.html', itemsSold=itemsSold)

@app.route('/edit_sold_records/<int:id>/', methods=['GET', 'POST'])
def editSoldRecords(id):
    # id is from the displaySoldRecords.html
    modifySold = SalesOfItems.query.get(id)
    _dates = DatesOfGames.query.all()
    names = MerchandiseItems.query.all()

    if request.method == 'POST':
        date_id = int(request.form['date_selected'])
        item_id = int(request.form['name_selected'])
        qty = int(request.form['quantity'])
        price = request.form['price']

        if 'cancel' in request.form:
            flash('Transaction canceled!')
            return redirect(url_for('index'))

        elif 'delete' in request.form:
            db_session.delete(modifySold)
            db_session.commit()
            flash('Record deleted!')
            return redirect(url_for('displaySoldRecords'))

        else:
            # print('date', date_id, 'item', item_id, 'qty', qty, 'price', price)
            # print('modidfadsf', modifySold, modifySold.date_id, modifySold.item_id)
            # The table takes a float for price, try/except is very handy here.
            try:
                price = float(price)

                if date_id == modifySold._date_id and \
                        item_id == modifySold.item_id and \
                        qty == modifySold.quantity_sold and \
                        price == modifySold.price_per_unit:
                    flash('Ther were no changes made!')
                    return redirect(url_for('displaySoldRecords'))

                elif date_id == modifySold._date_id and \
                        item_id == modifySold.item_id and \
                        qty != modifySold.quantity_sold or \
                        price != modifySold.price_per_unit:
                    modifySold.quantity_sold = qty
                    modifySold.price_per_unit = price
                    db_session.commit()
                    flash('Either quantity or price were updated!')
                    return redirect(url_for('displaySoldRecords'))
                else:
                    no_matched = True
                    for row in SalesOfItems.query.all():
                        if date_id == row._date_id and item_id == row.item_id:
                            no_matched = False
                            flash('{} and {} already in sold rec "{}" and "{}"'.format(date_id, item_id, modifySold, row))
                            return render_template('editSoldRecords.html', _dates=_dates, names=names, modifySold=modifySold)
                    if no_matched:
                        modifySold._date_id = date_id
                        modifySold.item_id = item_id
                        modifySold.quantity_sold = qty
                        modifySold.price_per_unit = price
                        db_session.commit()
                        flash('Data was updated succesfully!!')
                        return redirect(url_for('displaySoldRecords'))
            except Exception as e:
                db_session.rollback()
                flash('Error  <br>'+ str(e))
                return redirect(url_for('displaySoldRecords'))

    return render_template('editSoldRecords.html', \
                            modifySold=modifySold, _dates=_dates, \
                            names=names)
