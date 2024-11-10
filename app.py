from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)
ma = Marshmallow(app)

#===== building the three main commands to build, delete, seeding the database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created successfully!')

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(name='Mercury', type='Class D', home_star='Sol', mass=3.258e23, radius=1516, distance=35.98e6)
    venus = Planet(name='Venus', type='Class K', home_star='Sol', mass=4.867e24, radius=3760, distance=67.24e6)
    earth = Planet(name='Earth', type='Class M', home_star='Sol', mass=5.972e24, radius=3959, distance=92.96e6)

    db.session.add_all([mercury, venus, earth])

    test_user = User(first_name='Motasem', last_name='Ali', email='motasem@gmail.com', password='123@side.ps')
    db.session.add(test_user)

    db.session.commit()
    print('Database seeded successfully!')

#===== building API endpoints
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

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    return jsonify()


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

#===== building the models schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type', 'home_star', 'mass', 'radius', 'distance')

if __name__ == '__main__':
    app.run()
