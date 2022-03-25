"""Flask Login Example and instagram fallowing find"""

from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_utils


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    """ Create user table"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    def __init__(self, username, password, admin):
        self.username = username
        self.password = password
        self.admin = admin


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        user_data=User.query.all()
        if (request.method == "POST") and ('form1' in request.form):
            for user in User.query.all():
                user.admin=False
                db.session.commit()
            for idAdmin in request.form.getlist('mycheckbox'):
            #    print(idAdmin)
                User.query.filter_by(id=idAdmin).first().admin=True
                db.session.commit()
                #print(User.query.filter_by(id=idAdmin).first().admin)
            return "Done"
        return render_template('index.html',data=user_data)


@app.route('/get-json1')
def get_json1():
    try:
        return render_template('json_files/frst_1')

    except Exception as e:
        return str(e)


@app.route('/get-json2')
def get_json2():
    try:
        return render_template('json_files/second_1')

    except Exception as e:
        return str(e)


@app.route('/get-json3')
def get_json3():
    try:
        return render_template('json_files/trd_1')

    except Exception as e:
        return str(e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username=name, password=password).first()
            if data is not None:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return 'Dont Login'
        except:
            return "Dont Login"


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        if sqlalchemy_utils.database_exists('sqlite:///test.db'):
            new_user = User(
                admin=False,
                username=request.form['username'],
                password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
        else:
            new_user = User(
                admin=True,
                username=request.form['username'],
                password=request.form['password'])
            db.session.add(new_user)
            db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route("/logout")
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
    