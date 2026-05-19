from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='client') # admin, hotelier, client
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False) # hotel, auberge, residence
    stars = db.Column(db.Integer, default=0)
    city = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200))
    whatsapp = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    website = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    price_base = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.String(200)) # comma separated
    rooms = db.relationship('Room', backref='hotel', lazy=True)
    bookings = db.relationship('Booking', backref='hotel', lazy=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # Standard, Luxe, Suite
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='room', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    guest_phone = db.Column(db.String(20), nullable=False)
    guest_email = db.Column(db.String(100), nullable=True)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    advance_paid = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='pending') # pending, confirmed, cancelled
    qr_code_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
