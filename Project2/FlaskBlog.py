from flask import Flask, render_template, url_for
app = Flask(__name__)


posts = [
    {
        'author': 'Mohamed Mamdouh',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'May 18, 2019'
    },
    {
        'author': 'Tarek Mamdouh',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'May 05, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.debug = True
    app.run('', 5000)
