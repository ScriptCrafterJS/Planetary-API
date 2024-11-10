from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)

#===== building the three main commands to build, delete, seeding the database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database successfully created!')

#===== building the API endpoints
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Palnetary API.')

@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message=f'Sorry {name} you are not old enough.'), 401
    else:
        return jsonify(message=f'Hello {name} you are good to go.')

@app.route('/url_vars/<string:name>/<int:age>')
def url_vars(name: str, age: int):
    if age < 18:
        return jsonify(message=f'Sorry {name} you are not old enough.'), 401
    else:
        return jsonify(message=f'Hello {name} you are good to go.')


#===== building database models

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Planet(db.Model):
    __tablename__ = 'planets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)#is it habitable or not, has life or not
    home_star = Column(String)#to store what start this plant is orbiting
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)

if __name__ == '__main__':
    app.run()
