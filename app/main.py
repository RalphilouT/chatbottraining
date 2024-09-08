from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid 
import jwt
# from datetime import datetime, timedelta
import datetime
from functools import wraps
from flask_cors import CORS, cross_origin
from chat import get_response
# from security import login_required
# from vardata import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# Frontend not tied with flask 
engine = create_engine("sqlite:///app/api.db", echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    public_id = Column(Integer)
    name = Column(String)
    password = Column(String)
    def __init__(self, name):
        self.name = name    

Base.metadata.create_all(engine)

app = Flask(__name__)
CORS(app)
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DATABASE = os.path.join(PROJECT_ROOT, 'tmp', 'api.db')

app.config['SECRET_KEY']='F`_E1U]?02yqm-4@[DJ5GFmp1MigcrLCO?a81{R3\FCiv<Xb2'
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////api.db"
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(basedir, "api.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True 

db = SQLAlchemy()
db.init_app(app)

class Users(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer)  
    name = db.Column(db.String())
    password = db.Column(db.String())


# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return make_response(jsonify({"message": "Invalid token!"}), 401)
         # Return the user information attached to the token
        return f(*args, **kwargs)
    return decorator

         

@app.post("/predict")
@cross_origin(origins="*")
@token_required
def predict():
    text = request.get_json().get("message")
    if(text):
        resp = get_response(text)
        message = {"answer": resp}
        return jsonify(message)

@app.route('/register', methods=['GET', 'POST'])
@cross_origin(origins="*")
def signup_user():  
    data = request.get_json()  
    user = Users.query.filter_by(name=data['name']).first()
    if user:
        return make_response('Username is taken' , 401, {'WWW-Authenticate': 'Basic-realm= "Username taken!"'}) 
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    
    new_user = Users(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password) 
    db.session.add(new_user)  
    db.session.commit()    

    return jsonify({'message': 'registered successfully'})

@app.route('/login', methods=['GET', 'POST'])  
@cross_origin(origins="*")
def login_user(): 
    auth = request.authorization   

    if not auth or not auth.username or not auth.password:  
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

    user = Users.query.filter_by(name=auth.username).first() 
    if not user:
        return make_response('Could not verify user, Please signup!', 401, {'WWW-Authenticate': 'Basic-realm= "No user found!"'})
      
    if check_password_hash(user.password, auth.get('password')): 
        token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], 'HS256') 
        
        return make_response(jsonify({'token': token}), 201)

    return make_response('Could not verify',  401, {'WWW Authentication': 'Basic realm: "Login required"'})

@app.route('/user', methods=['GET'])
@cross_origin(origins="*")
def get_all_users():  
   
   users = Users.query.all() 

   result = []   

   for user in users:   
       user_data = {}   
       user_data['public_id'] = user.public_id  
       user_data['name'] = user.name 
       user_data['password'] = user.password
       
       result.append(user_data)   

   return jsonify({'users': result})  


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)



