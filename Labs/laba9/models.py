from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_code = db.Column(db.String(3), nullable=False)
    char_code = db.Column(db.String(3), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    nominal = db.Column(db.Integer, nullable=False)

class UserCurrency(db.Model):
    __tablename__ = 'user_currency'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('currencies', lazy=True))
    currency = db.relationship('Currency', backref=db.backref('users', lazy=True))