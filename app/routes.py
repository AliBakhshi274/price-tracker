import random
from flask import render_template, redirect, url_for, flash, jsonify
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
            email=form.email.data,
            password=hashed_password
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
    # randomly change the product_id ....
    random_product = random.choice(products)
    product, common_chart_data = views.common_product_chart(random_product.id)
    forecast_data = views.forecast_product_chart(random_product.id)
    return render_template(
        'dashboard/dashboard.html',
        products=products,
        product=product,
        common_chart_data=common_chart_data,
        forecast_data=forecast_data
    )


@app.route('/product_data/<int:product_id>', methods=['GET', 'POST'])
@login_required
def product_data(product_id):
    product, common_chart_data = views.common_product_chart(product_id)
    forecast_data = views.forecast_product_chart(product_id)
    return jsonify({
        'common_chart_data': common_chart_data,
        'forecast_data': forecast_data,
        'product': {'name': product.name}
    })
