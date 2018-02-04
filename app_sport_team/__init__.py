from flask import Flask, session, g, render_template

app = Flask(__name__)
app.config.from_object('website_config')

# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404  # TODO: Create a 404.html file in templates dir.

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()

# TODO: create views file and attributes.
from app_sport_team.views import routes
# etc.

# TODO: get register_blueprint/create files.
# app.register_blueprint(routes.mod)
#etc

from app_sport_team.database_tables import db_session, Item, Schedule, \
 Quantitysold

# TODO: check the code below and fix it
# from app_sport_team import utils #TODO create utils.py
#
# app.jinja_env.filters['datetimeformat'] = utils.format_datetime
# app.jinja_env.filters['dateformat'] = utils.format_date
# app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
# app.jinja_env.filters['displayopenid'] = utils.display_openid
