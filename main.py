from flask import Flask, json,redirect,render_template,flash,request
from flask.globals import request, session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user

# from flask_mail import Mail
import json

# mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="suryaprakash"

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/coursezz'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

# defining database entity to store data

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    phone=db.Column(db.String(20),unique=True)
    email=db.Column(db.String(50))
    pwd=db.Column(db.String(1000))

@app.route("/")
def home():
   
    return render_template("index.html")

#verifying signup credential

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        phone=request.form.get('phone')
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        encpassword=generate_password_hash(pwd)
        user=User.query.filter_by(phone=phone).first()
        emailUser=User.query.filter_by(email=email).first()
        if user or emailUser:
            flash("Email is already taken","warning")
            return render_template("signup.html")
        # Inserting data into database
        new_user=db.engine.execute(f"INSERT INTO `user` (`phone`,`email`,`pwd`) VALUES ('{phone}','{email}','{encpassword}') ")
                
        flash("SignUp Success Please Login","success")
        return render_template("index.html")

    return render_template("signup.html")
