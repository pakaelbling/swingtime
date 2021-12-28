from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import wteSite.nearestNeighbor as nn
from wteSite.config import Config
import pytz

#Instantiate and add various utils
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
bcrypt = Bcrypt(app)
mail = Mail(app)
tz = pytz.timezone('America/New_York')

#Not user facing, used to set up the database on the host
util = Blueprint('util', __name__, url_prefix='/util')
@util.route("/db/create_all/")
def db_create_all():
    db.create_all()
    return "Database initialized :)"
app.register_blueprint(util)

def trivialDist(x,y):
    return x == y

#Predictors need a distance function, normalize both the time and date distance to [0, 1]
def betterDist(x,y):
    normalizedtime1, date1 = x
    normalizedtime2, date2 = y
    timeDist = abs(normalizedtime1 - normalizedtime2) / 540
    dateDist = min([abs(date1-date2),7-abs(date1-date2)]) / 3
    return timeDist + dateDist

from wteSite.models import Datapoint
#Instantiate predictor and populate it with stored datapoints
predictor = nn.nNearestNeighbor(betterDist, alpha=0.8,n=3)
loadedData = [((p.date_created, p.day_of_week),p.wait_time) for p in Datapoint.query.all()]
processed = [(((date.hour * 60 + date.minute - wait) - 11*60, day),wait) for ((date, day), wait) in loadedData]
[predictor.addDatum(key,val) for (key, val) in processed]
from wteSite import routes
