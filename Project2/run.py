from flaskblog import app

if __name__ == '__main__':
    app.debug = True
    app.run('', 5000)
