from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
import time

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('sign-in.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)

    return redirect(url_for('main.dashboard'))

@auth.route('/signup')
def signup():
    return render_template('new-old/signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/resetpassword')
def resetpassword():
    return render_template('new-old/newpassword.html')


@auth.route('/resetpassword', methods=['POST'])
def resetpassword_post():
    userEmail = request.form.get('email')
    oldUser = User.query.filter_by(email=userEmail).first()
    print(oldUser)
    oldPassword = request.form.get('oldpassword')
    print(oldPassword)
    newPassword = request.form.get('newpassword')
    print(newPassword)
    confirmNewPassword = request.form.get('confirmnewpassword')
    if not check_password_hash(oldUser.password, oldPassword):
        flash('The old password is incorrect.')
        return redirect(url_for('auth.resetpassword'))
    if not newPassword == confirmNewPassword:
        flash('The new passwords do not match.')
        return redirect(url_for('auth.resetpassword'))
    if newPassword == oldPassword:
        flash('The old password and the new password match.')
        return redirect(url_for('auth.resetpassword'))

    newUser = User(email=userEmail, name=oldUser.name, password=generate_password_hash(newPassword, method='sha256'))
    print(newUser)
    print(oldUser)
    db.session.delete(oldUser)
    db.session.add(newUser)
    db.session.commit()

    return redirect(url_for('main.dashboard'))
