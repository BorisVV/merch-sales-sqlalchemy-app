from app_sport_team import app
from app_sport_team.tables_setUp import db_session, MerchandiseItems
from flask import render_template, redirect, url_for, g, abort, request, flash

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/home/')
def home():
    return render_template('home.html', items = MerchandiseItems.query.all())

@app.route('/home/add_items', methods=['GET', 'POST'])
def addItems():
    if request.method == 'POST':
        if 'cancel' in request.form:
            return redirect(url_for('home'))
        new_item = request.form['name']
        if 'continue' and not new_item:
            flash('Error: name is required')
        else:
            db_session.add(MerchandiseItems(name=new_item))
            db_session.commit()
            return redirect(url_for('home'))
    return render_template('addItems.html', items = MerchandiseItems.query.all())

@app.route('/home/edit', methods=['GET', 'POST']) #/<int:id>/
def edit():
    items = MerchandiseItems.query.all()
    # form = dict(name=item_id.name)
    if request.method == 'POST':
        rm_id = MerchandiseItems.query.get(request.form['item_id'])
        if 'delete' in request.form:
            db_session.delete(rm_id)
            db_session.commit()
            flash(u'Item deleted')
            return redirect(url_for('home'))
        elif 'cancel' in request.form:
            return redirect(url_for('home'))
    return render_template('edit.html', items=items)
