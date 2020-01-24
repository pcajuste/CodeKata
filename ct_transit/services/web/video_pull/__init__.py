from flask import Flask, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, RadioField, SelectField, DateField, DateTimeField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, InputRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
#from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object("video_pull.config.Config")
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mail = Mail(app)

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('EmployeeRole', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True)
    password= db.Column(db.String(80))
    roles = db.relationship('EmployeeRole', backref='employee')
    hddata = db.relationship('BusHD', backref='employee')

    def __repr__(self):
        return '<User %r>' % self.username


class EmployeeRole(db.Model):
    __tablename__ = 'emp_role_xref'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), index=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), index=True)

    def __repr__(self):
        return '<EmployeeRole %r>' % self.role_id, self.employee_id


class Bus(db.Model):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)
    bus_num = db.Column(db.String(8), unique=True, index=True)
    drives = db.relationship('BusHD', backref='bus')

    def __repr__(self):
        return '<Bus %r>' % self.bus_num, self.id


class HD(db.Model):
    __tablename__ = 'hard_drive'
    id = db.Column(db.Integer, primary_key=True)
    serial_num = db.Column(db.String(16), unique=True, index=True)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'), index=True)
    hd_out_bus = db.relationship('BusHD', foreign_keys="[BusHD.hd_out_id]")
    hd_in_bus = db.relationship('BusHD', foreign_keys="[BusHD.hd_in_id]")


    def __repr__(self):
        return '<HD %r>' % self.serial_num, self.id


class BusHD(db.Model):
    __tablename__ = 'bus_hd_xref'
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), index=True)
    hd_out_id = db.Column(db.Integer, db.ForeignKey('hard_drive.id'), index=True)
    hd_in_id = db.Column(db.Integer, db.ForeignKey('hard_drive.id'), index=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), index=True)
    reason_id = db.Column(db.Integer, db.ForeignKey('reason.id'), index=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    notes = db.Column(db.String(256))

    def __repr__(self):
        return '<BusHD %r>' % self.bus_id, self.hd_out, self.hd_in, self.id


class Reason(db.Model):
    __tablename__ = 'reason'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    hddata = db.relationship('BusHD', backref='reason')

    def __repr__(self):
        return '<Reason %r>' % self.name, self.id


class Condition(db.Model):
    __tablename__ = 'condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, index=True)
    HDs = db.relationship('HD', backref='condition')

    def __repr__(self):
        return '<Condition %r>' % self.name, self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm1(FlaskForm):
    email = StringField('Email?', validators=[DataRequired()])
    password = StringField('Password?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class VideoLogEntryForm(FlaskForm):
    bus = SelectField('Bus Number', validators=[DataRequired()])
    supervisor = SelectField('Supervisor', validators=[DataRequired()])
    reason = SelectField('Situation', validators=[DataRequired()])
    hd_out = SelectField('Hard Drive Out', validators=[DataRequired()])
    hd_in = SelectField('Hard Drive In', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time= DateTimeField('Date', validators=[DataRequired()])
    notes = TextAreaField('Notes', validators=[Optional()])
    cancel = SubmitField('Cancel')
    save = SubmitField('Save')

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


#@app.route("/")
#def ct_transit():
    #return jsonify("Hello CT Transit")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/test', methods=['GET'])
def dropdown():
    colours = ['Red', 'Blue', 'Black', 'Orange']
    return render_template('test.html', colours=colours)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user sucessfuly created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + ' ' + hashed_password + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    #if form.validate_on_submit():
    # user = User.query.filter_by(username=form.name.data).first()
    #if user is None:
    #user = User(username=form.name.data)
    #db.session.add(user)
    #db.session.commit()
    #session['known'] = False
    #else:
    #session['known'] = True
    session['name'] = form.name.data
    #return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False))

@app.route('/dashboard')
@login_required
def dashboard():
    #return render_template('dashboard.html')
     return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route('/request', methods=['GET', 'POST'])
def request():
    form = VideoLogEntryForm()
    """ if form.validate_on_submit():
        bus = Bus.query.filter_by(bus_num=form.num.data).first()
        if bus is None:
            bus = Bus(bus_num=form.num.data)
            db.session.add(bus)
            db.session.commit()
            session['known'] = False
        else:
            #session['known'] = True
            #session['name'] = form.num.data
           #return redirect(url_for('bus')) """
    return render_template('videolog.html', form=form,
                           known=session.get('known', False))

