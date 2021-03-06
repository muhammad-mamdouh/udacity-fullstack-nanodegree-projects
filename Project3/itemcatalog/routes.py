from flask import render_template, url_for, flash, redirect, request, abort, jsonify
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
    items = Item.query.order_by(Item.date_published.desc()).all()
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
        return redirect(url_for('category_items', category_id=category_id))
    return render_template('create_edit_item.html', title='New Category',
                           form=form, category=category, legend='New Item')


@app.route('/categories/<int:category_id>/items/<int:item_id>')
def item(category_id, item_id):
    category = Category.query.get_or_404(category_id)
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', title=item.name, category=category, item=item)


@app.route('/categories/<int:category_id>/items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(category_id, item_id):
    category = Category.query.get_or_404(category_id)
    item = Item.query.get_or_404(item_id)
    if item.item_author != current_user:
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        db.session.commit()
        flash('Your item has been updated!', 'success')
        return redirect(url_for('item', category_id=category.id, item_id=item.id))
    elif request.method == 'GET':
        form.name.data = item.name
        form.description.data = item.description
    return render_template('create_edit_item.html', title=f'Edit {item.name}',
                           category=category, item=item, form=form, legend='Update Item')


@app.route('/categories/<int:category_id>/items/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(category_id, item_id):
    category = Category.query.get_or_404(category_id)
    item = Item.query.get_or_404(item_id)
    if item.item_author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted successfully!', 'success')
    return redirect(url_for('home'))


@app.route('/categories/<int:category_id>/items')
def category_items(category_id):
    category = Category.query.filter_by(id=category_id).one()
    items = Item.query.filter_by(category_id=category_id).order_by(Item.date_published.desc()).all()
    last_item = Item.query.filter_by(category_id=category_id).order_by(Item.date_published.desc()).first()
    return render_template('home.html', items=items,
                           category_id=category_id, category=category, last_item=last_item)


@app.route('/items/JSON')
def categories_json():
    """Return JSON for all of the categories"""
    items = Item.query.all()
    return jsonify(items=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/items/JSON')
def category_items_json(category_id):
    """Return JSON for all of the items of a specific category"""
    category_items = Item.query.filter_by(category_id=category_id).all()
    return jsonify(category_items=[i.serialize for i in category_items])


@app.route('/categories/JSON')
def items_json():
    """Return JSON for all of the items"""
    categories = Category.query.all()
    return jsonify(categories=[i.serialize for i in categories])
