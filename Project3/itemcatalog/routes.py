from flask import render_template, url_for, flash, redirect
from itemcatalog import app, db, bcrypt
from itemcatalog.forms import RegistrationForm, LoginForm
from itemcatalog.models import User, Category, Item
from flask_login import login_user, logout_user, current_user


items = [
    {
        'author': 'Mohamed Mamdouh',
        'title': 'Snowboard',
        'description': 'Description for the first item.',
        'category': 'Soccer',
        'date_published': 'May 18, 2019'
    },
    {
        'author': 'Tarek Mamdouh',
        'title': 'Stick',
        'description': 'Description for the second item.',
        'category': 'Hockey',
        'date_published': 'May 05, 2019'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', items=items)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
