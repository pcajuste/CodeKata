from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("video_pull.config.Config")
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('UserRole', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('UserRole', backref='user', lazy='dynamic')
    hddata = db.relationship('bus_hd_xref', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

class UserRole(db.Model):
    __tablename__ = 'user_role_xref'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

    def __repr__(self):
        return '<UserRole %r>' % self.role_id, self.user_id


class Bus(db.Model):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)
    bus_num = db.Column(db.String(8), unique=True, index=True)
    drives = db.relationship('bus_hd_xref', backref='bus')

    def __repr__(self):
        return '<Bus %r>' % self.bus_num, self.id

class HD(db.Model):
    __tablename__ = 'hard_drive'
    id = db.Column(db.Integer, primary_key=True)
    serial_num = db.Column(db.String(16), unique=True, index=True)
    condition = db.Column(db.Boolean)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), index=True)
    buses = db.relationship('bus_hd_xref', backref='hd')

    def __repr__(self):
        return '<HD %r>' % self.serial_num, self.id

class BusHD(db.Model):
    __tablename__ = 'bus_hd_xref'
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), index=True)
    hd_id = db.Column(db.Integer, db.ForeignKey('hard_drive.id'), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), index=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    notes = db.Column(db.String(256))

    def __repr__(self):
        return '<BusHD %r>' % self.bus_id, self.hd_id, self.id

class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, index=True)
    HDs = db.relationship('HD', backref='status')
    hddata= db.relationship('bus_hd_xref', backref='status')

    def __repr__(self):
        return '<Status %r>' % self.name, self.id

class condition(db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, index=True)
    HDs = db.relationship('HD', backref='status')

    def __repr__(self):
        return '<Status %r>' % self.name, self.id



@app.route("/")
def ct_transit():
    return jsonify("Hello CT Transit")
