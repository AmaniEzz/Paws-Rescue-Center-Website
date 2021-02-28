from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from marshmallow_sqlalchemy import ModelSchema, SQLAlchemyAutoSchema
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

"""Model for Pets."""
class Pet(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age  = db.Column(db.String, nullable=False)
    bio  = db.Column(db.String, nullable=False)
    image  = db.Column(db.String, nullable=True)
    adopted  = db.Column(db.Boolean, nullable=False, default=False)
    #create a forgien key from Users class
    adopted_by = db.Column(db.String, db.ForeignKey('user.id'),  default="None")

class PetSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pet
        sqla_session = db.session

"""Model for Users."""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    #set one-to-many relationship between users and pets
    #This back-reference will enable us to point to a row in User by using pet.user.
    pets = db.relationship('Pet', backref = 'user')

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
