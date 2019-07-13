from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

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
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
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


if __name__ == '__main__':
    app.debug = True
    app.run('', 8000)
