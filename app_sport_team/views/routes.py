
from flask import \
        render_template, redirect, url_for, g, abort, request, flash, \
        Response

from app_sport_team import app
from app_sport_team.tables_setUp import \
            db_session, MerchandiseItems, SalesOfItems, DatesOfGames


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home/')
def home():
    items = MerchandiseItems.query.all()
    return render_template('home.html', items=items)

@app.route('/home/add_items/', methods=['GET', 'POST'])
def addItems():
    items = MerchandiseItems.query.all()
    if request.method == 'POST':
        new_name = request.form['name'].capitalize()
        if 'cancel' in request.form:
            return redirect(url_for('home'))

        isIn = False
        for name in items:
            if new_name == name.name:
                flash(u'That name is already in file. <br>Try a different one')
                isIn = True
                return redirect(url_for('addItems'))
        if new_name != "" and isIn == False:
            db_session.add(MerchandiseItems(name=new_name))
            db_session.commit()
            flash(u'Success! %r was added' % new_name)
            return redirect(url_for('home'))

        else:
            flash(u'Cannot be blank')
    return render_template('addItems.html', items=items)


@app.route('/editItems/', methods=['GET', 'POST']) #/<int:id>/
def editItems():
    items = MerchandiseItems.query.all()

    if request.method == 'POST':
        rm_id = MerchandiseItems.query.get(request.form['_item'])
        new_name = request.form['new_name']
        if 'delete' in request.form:
            db_session.delete(rm_id)
            db_session.commit()
            flash(u'Item deleted')
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
    dates = DatesOfGames.query.all()

    if request.method == 'POST':
        date_game = request.form['date_game']

        city = request.form['city']
        state = request.form['state']

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        else:
            if date_game == '' or city == '' or state == '':
                flash('No blank text boxes allowed!')
                return render_template('addDates.html', date_game=date_game, \
                                city=city, state=state)

            for _date in dates:
                if _date.game_date == date_game:
                    flash(u'Date {} is already in file it can\'t be used twice!'.format(date_game))
                    return render_template('addDates.html',\
                        date_game=date_game, city=city, state=state)

            db_session.add(DatesOfGames(game_date=str(date_game), city=city, state=state))
            db_session.commit()
            flash('Success! <br> Date: {}, City: {}, State: {}, was added to'\
                    '<br> Games\'s Schedules'.format(date_game, city, state))
            return redirect(url_for('home'))

    return render_template('addDates.html', dates=dates)


@app.route('/show_dates/', methods=['GET', 'POST'])
def show_dates():
    dates = DatesOfGames.query.all()
    return render_template('show_dates.html', dates=dates)
