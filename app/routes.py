from flask import render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db, app
from app.forms import LoginForm, RegistrationForm
from app.models import User, Product
from flask_login import login_user, logout_user, current_user, login_required
import app.views as views

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

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
        return redirect(url_for('login'))
    return render_template('login/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You are now logged in.', 'success')
            return redirect(url_for('dashboard'))

    flash('Invalid username or password.', 'danger')
    return render_template('login/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out.', 'success')
    return redirect(url_for('register'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    products = Product.query.all()
    # manually changed ....
    product , chart_data = views.product_chart(20)
    return render_template(
        'dashboard/dashboard.html',
        products=products,
        product=product,
        chart_data=chart_data
    )

















































