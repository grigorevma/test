from . import db


class Billing(db.Model):
    __tablename__ = 'billing'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, unique=False)
    currency = db.Column(db.String(64), unique=False)
    description = db.Column(db.String(64), unique=False)
    purchases_date = db.Column(db.String(64), unique=False)
