from flask import Flask
from flask import render_template

app = Flask(__name__)


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
    return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run('', 8000)
