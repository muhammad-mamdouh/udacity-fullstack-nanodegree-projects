from flask import render_template, url_for, flash, redirect, request
from itemcatalog import app, db, bcrypt
from itemcatalog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                               CategoryForm, ItemForm)
from itemcatalog.models import User, Category, Item
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os


@app.route('/')
@app.route('/home')
def home():
    items = Item.query.all()
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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    form_picture.save(picture_path)

    return picture_filename


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/categories/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category has been added successfully!', 'success')
        return redirect(url_for('show_categories'))
    return render_template('create_category.html', title='New Category', form=form)


@app.route('/categories')
def show_categories():
    categories = Category.query.all()
    return render_template('show_categories.html', title='All Categories', categories=categories)


@app.route('/categories/<int:category_id>/items/new', methods=['GET', 'POST'])
@login_required
def new_item(category_id):
    category = Category.query.filter_by(id=category_id).one()
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(name=form.name.data, description=form.description.data,
                    item_author=current_user, item_category=category)
        db.session.add(item)
        db.session.commit()
        flash('Item has been added successfully!', 'success')
        return redirect(url_for('show_categories'))
    return render_template('create_item.html', title='New Category', form=form, category=category)
