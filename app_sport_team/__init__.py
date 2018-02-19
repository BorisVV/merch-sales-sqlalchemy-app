from flask import Flask, session, g, render_template

app = Flask(__name__)
app.config.from_object('web_config')

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()

# # @app.errorhandler(404)
# # def not_found(error):
# #     return render_template('404.html'), 404  # TODO: Create a 404.html file in templates dir.

# TODO: create views file and attributes.
from app_sport_team.views import routes
# etc.

# # TODO: get register_blueprint/create files.
# # app.register_blueprint(routes.mod)
# #etc

from app_sport_team.tables_setUp import db_session, MerchandiseItems, SalesOfItems, DatesOfGames

# # TODO: check the code below and fix it
# # from app_sport_team import utils #TODO create utils.py
# #
# # app.jinja_env.filters['datetimeformat'] = utils.format_datetime
# # app.jinja_env.filters['dateformat'] = utils.format_date
# # app.jinja_env.filters['timedeltaformat'] = utils.format_timedelta
# # app.jinja_env.filters['displayopenid'] = utils.display_openid
