from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from app import db, app
from app.forms import LoginForm, RegistrationForm
from app.models import User
from flask_login import login_user, logout_user, current_user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(
            username=form.username.data,
            email = form.email.data,
            password = hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created. You are now able to log in.', 'success')
        return redirect(url_for('login', form=form))
    return render_template(
        'register.html',
        form=form,
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You are now logged in.', 'success')
            return redirect(url_for('dashboard'))

    flash('Invalid username or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('register'))




















































