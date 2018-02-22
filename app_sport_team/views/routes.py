from flask import render_template, redirect, url_for, g, abort, request, flash
from app_sport_team import app
from app_sport_team.tables_setUp import db_session, \
                                        MerchandiseItems, \
                                        SalesOfItems, \
                                        DatesOfGames


@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home/')
def home():
    return render_template('home.html', items = MerchandiseItems.query.all())

@app.route('/home/add_items', methods=['GET', 'POST'])
def addItems():
    if request.method == 'POST':
        new_item = request.form['name']
        if 'cancel' in request.form:
            return redirect(url_for('home'))

        else:
            if new_item != "":
                db_session.add(MerchandiseItems(name=new_item))
                db_session.commit()
                return redirect(url_for('home'))
    return render_template('addItems.html', items = MerchandiseItems.query.all())

@app.route('/home/add_dates', methods=['GET', 'POST'])
def addDates():
    dates = DatesOfGames.query.all()
    form = dict(date='date', city='city', state='state')
    if request.form == 'POST':
        form['date'] = request.form['date']
        form['city'] = request.form['city']
        form['state'] = request.form['state']

        if 'cancel' in request.form:
            return redirect(url_for('home'))

        else:
            db_session.add(DatesOfGames(game_date=str(form['date']), city=form['city'], state=form['state']))
            db_session.commit()
            return redirect(url_for('home'))
    return render_template('addDates.html', dates=dates, form=form)

@app.route('/home/editItems', methods=['GET', 'POST']) #/<int:id>/
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


@app.route('/home/show_dates', methods=['GET', 'POST'])
def show_dates():
    dates = DatesOfGames.query.all()
    return render_template('show_dates.html', dates=dates)
