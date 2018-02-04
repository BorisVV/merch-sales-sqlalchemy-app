from app_sport_team import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello World"
