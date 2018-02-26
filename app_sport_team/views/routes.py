
from flask import \
        render_template, redirect, url_for, g, abort, request, flash, \
        Response

from app_sport_team import app
from app_sport_team.tables_setUp import \
            db_session, MerchandiseItems, SalesOfItems, DatesOfGames

# Query all the merchandise items.
def items_query():
    return MerchandiseItems.query.all()

# Query all the game's dates.
def dates_query():
    return DatesOfGames.query.all()


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home/')
def home():
    items = items_query()
    return render_template('home.html', items=items)

@app.route('/home/add_items/', methods=['GET', 'POST'])
def addItems():
    items = items_query()
    if request.method == 'POST':
        new_name = request.form['name'].capitalize()
        if 'cancel' in request.form:
            return redirect(url_for('home'))

        if new_name == "":
            flash(u'Oops! It cannot be blank')
            return redirect(url_for('addItems'))

        name_in_table = False
        for name in items:
            if new_name == name.name:
                flash(u'Name %r already exist. <br>Try a different one' % new_name)
                name_in_table = True
                return redirect(url_for('addItems'))

        if name_in_table == False:
            db_session.add(MerchandiseItems(name=new_name))
            db_session.commit()
            flash(u'Success! %r was added.' % new_name + u'<br>Do you want ' \
                    'to add another one? "Cancel to exit"')
            return redirect(url_for('addItems'))

    return render_template('addItems.html', items=items)


@app.route('/editItems/', methods=['GET', 'POST']) #/<int:id>/
def editItems():
    items = items_query()
    if request.method == 'POST':
        rm_id = MerchandiseItems.query.get(request.form['_item'])
        new_name = request.form['new_name']
        if 'delete' in request.form:
            db_session.delete(rm_id)
            db_session.commit()
            flash(u'%r was deleted' % rm_id)
            return redirect(url_for('home'))
        if 'update' in request.form:
            if new_name != "":
                rm_id.name = new_name
                db_session.commit()
                return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))
    return render_template('editItems.html', items=items)

@app.route('/addDates/', methods=['GET', 'POST'])
def addDates():
    _dates = dates_query()

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
