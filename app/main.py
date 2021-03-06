from flask import Flask, render_template, request, redirect, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] #for running on heroku
except KeyError:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #for localhost

app.config['DEBUG'] = True #get some debugging output on crash
app.secret_key = 'WOW SUCH SECRET'
db = SQLAlchemy(app) #bind database to app

class User(db.Model):
    """
    database schema for users
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    pwd_hash = db.Column(db.String(180))
    
    def __init__(self, username, password):
        self.username = username
        self.pwd_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def __repr__(self):
        return '<User %r>: %r' % (self.username, self.pwd_hash)


@app.route("/")
def index():
    """
    Will allow users to log in/register. Once logged in, take them to profile home page
    """
    if 'username' in session:
        return redirect(url_for('profile'))
    else:
        return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    """
    handle logging the user in
    """
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['pwd']
        u = User.query.filter_by(username=uname).first() #get the user based on username
        if u is None:
            return render_template("index.html", error="No such username!")
        if u.check_password(pwd):
            session['username'] = uname
            return redirect(url_for("profile"))
        else:
            return render_template("index.html", error="Wrong password!")
    else:
        if 'username' in session:
            return redirect(url_for("profile"))
        return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    """
    handle registering the user
    """
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['pwd']
        
        if User.query.filter_by(username=uname).first():
            return render_template("register.html", error="Username already taken!")

        new_user = User(uname, pwd)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("index"))
    else:
        return render_template("register.html")


@app.route("/profile")
def profile():
    """
    handle loading the profile page once user is logged in
    """
    if 'username' in session:
        return render_template("profile.html")
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    """
    handle logging the user out
    """
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/view_users')
def view_users():
    """
    debugging view for looking at users in database
    """
    return render_template("view_users.html", data=User.query.order_by(User.username))
        
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
   
