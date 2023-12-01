from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Session(db.Model):
    # Session information
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    browser = db.Column(db.String(50))
    device = db.Column(db.String(50))
    ip = db.Column(db.String(50))
    query_counter = db.Column(db.Integer)

    # User information
    user_id = db.Column(db.String(50))
    username = db.Column(db.String(50))
    country = db.Column(db.String(50))
    city = db.Column(db.String(50))
    clicks = db.relationship('Click', backref='session', lazy=True)
    requests = db.relationship('Request', backref='session', lazy=True)

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    doc_id = db.Column(db.String(50))
    click_type = db.Column(db.String(20))

class Request(db.Model):
    # I want a table that contains the information requested by the user named as query
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    query_terms = db.Column(db.String(255))
    search_algorithm = db.Column(db.String(30))
