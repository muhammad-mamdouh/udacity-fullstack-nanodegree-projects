from flask import render_template, url_for, flash, redirect
from itemcatalog import app, db, bcrypt
from itemcatalog.forms import RegistrationForm, LoginForm
from itemcatalog.models import User, Category, Item


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
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)
