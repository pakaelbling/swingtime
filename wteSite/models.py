from wteSite import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Represents user submitted datapoints
class Datapoint(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    date_created = db.Column(db.DateTime(), nullable=False)
    wait_time = db.Column(db.Integer(), nullable=False)
    day_of_week = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"Wait time at {self.date_created} reported as {self.wait_time} and day {self.day_of_week}"


#Represents a user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    points = db.relationship('Datapoint', backref='submitter',lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"