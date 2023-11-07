from main import db, app, UserMixin
from flask_bcrypt import Bcrypt
import datetime

bcrypt = Bcrypt(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String,nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    address = db.Column(db.String)
    phone = db.Column(db.String)
    profile_pic_url = db.Column(db.String, default='static/blankprof.jpg')
    cars = db.relationship('Car', backref='user', lazy=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    manufactured = db.Column(db.Integer, nullable=False)
    milage = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.Integer, nullable=False)
    added = db.Column(db.DateTime, default=datetime.datetime.now())
    sold = db.Column(db.DateTime)
    power = db.Column(db.Integer) #in KW
    engine = db.Column(db.Float) #volume in liters
    doors = db.Column(db.Integer)
    steering = db.Column(db.String, default='left wheel')
    gearbox = db.Column(db.String, default='manual')
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photos = db.relationship('CarPhoto', backref='car', lazy=True)
    ac = db.Column(db.Boolean, default=False)
    stereo = db.Column(db.Boolean, default=False)
    awd = db.Column(db.Boolean, default=False)
    satnav = db.Column(db.Boolean, default=False)
    abs = db.Column(db.Boolean, default=False)
    esp = db.Column(db.Boolean, default=False)
    cruize_control = db.Column(db.Boolean, default=False)
    airbag = db.Column(db.Boolean, default=False)
    electric_windows = db.Column(db.Boolean, default=False)
    central_locking = db.Column(db.Boolean, default=False)
    alloy_wheels = db.Column(db.Boolean, default=False)
    info = db.Column(db.String)

class CarPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String, default='')
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)


# with app.app_context():
#     db.create_all()