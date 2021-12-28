from wteSite import app, db, bcrypt, predictor, mail, tz
from flask import render_template, url_for, request, flash, redirect
from datetime import datetime
from flask_login import current_user, logout_user, login_user, login_required
from wteSite.forms import DatapointForm, LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from wteSite.models import Datapoint, User
from wteSite.util import date_transform_query, date_transform_point
from flask_mail import Message

#These functions define the behaviour for the various pages in the website, ultimately rendering the templates seen in ./templates
#and providing them with the necessary dynamic information.

@app.route("/")
@app.route("/home")
def home():
    currentEstimate = predictor.predict(key = (date_transform_query(datetime.now(tz=tz)),datetime.today().weekday())) #FIXME need to transform the query
    currTime = datetime.now(tz=tz)
    points = Datapoint.query.all()
    return render_template('home.html',est=currentEstimate, time=currTime, points=points)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@login_required
@app.route("/enter_point",methods=['GET','POST'])
def enter_point():
    form = DatapointForm()
    if form.validate_on_submit():
        point = Datapoint(day_of_week=datetime.today().weekday(),date_created=datetime.now(tz=tz),wait_time=form.wait_time.data, submitter=current_user)
        db.session.add(point)
        db.session.commit()
        predictor.addDatum((date_transform_point(datetime.now(tz=tz),wait=form.wait_time.data),datetime.today().weekday()), form.wait_time.data)
        flash(f"Datapoint submitted! Thank you :-)", "success")
        return redirect(url_for('home'))
    return render_template('enter_point.html',title="Data Entry", form = form)

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}! You can now log in.", category="success")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("login failed. check email & password", "danger")
    return render_template('login.html', title="Log in", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Account updated successfully!", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title="Account", form = form)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f"""
To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, ignore this email and maybe change your password.
"""
    mail.send(msg)

@app.route("/reset_password", methods = ['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with reset instructions.", "info")
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password", form=form)

@app.route("/reset_password/<token>", methods = ['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.hello'))
    user = User.verify_reset_token(token)
    if not user:
        flash("that is an invalid or expired token", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashedPassword
        db.session.commit()
        flash(f"Password successfully changed for {form.username.data}! You can now log in with your new password.", category="success")
        return redirect(url_for('login'))
    return render_template('reset_token.html',title="Reset Password", form=form)