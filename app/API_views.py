from flask import Flask, render_template, abort,session,redirect,url_for, jsonify
from flask import make_response
from flask import request
from admin import setup_admin
from models import db, User, Pet, PetSchema, UserSchema

from flask import Blueprint


pet_api = Blueprint('api', __name__)
       

@pet_api.route("/pets/api/v1.0/pets", methods=['GET'])
def get_all():
    All_Pets =  Pet.query.all()
    
    # Serialize all data for the response
    Pet_schema = PetSchema(many=True)
    return jsonify(Pet_schema.dump(All_Pets))


@pet_api.route('/pets/api/v1.0/details/<int:pet_ID>', methods=['GET'])
def get_a_pet(pet_ID):
    pet = Pet.query.get(pet_ID)

    if pet is not None:
        Pet_schema = PetSchema()
        return Pet_schema.dump(pet)
    else:
        abort(404, 'Pet not found for Id: {pet_ID}'.format(pet_ID=pet_ID))


@pet_api.route('/pets/api/v1.0/create', methods=['POST'])
def Newpet():
       name = request.json.get('name', '')
       age = request.json.get('age', '')
       bio = request.json.get('bio', '')
       
       new_pet = Pet(name = name, age=age, bio=bio)
       
       db.session.add(new_pet)
       db.session.commit()

       Pet_schema = PetSchema()
       return Pet_schema.dump(new_pet)


@pet_api.route('/pets/api/v1.0/update/<int:pet_ID>/<string:field>', methods=['PATCH'])
def update_pet_info(pet_ID, field):

    updated_pet = Pet.query.get(pet_ID)

    if field == "all":
        name = request.json.get('name', '')
        age  = request.get('ages', '')
        bio  = request.get('bio', '')
        updated_pet.name = name
        updated_pet.age = age
        updated_pet.bio = bio

    elif field == "name":
        name = request.json.get('name', '')
        updated_pet.name = name

    elif field == "age":
        age = request.json.get('age', '')
        updated_pet.age = age

    elif field == "bio":
        bio = request.json.get('bio', '')
        updated_pet.bio = bio

    db.session.add(updated_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(updated_pet)


@pet_api.route('/pets/api/v1.0/delete/<int:pet_ID>/', methods=["DELETE"])
def delete_pet(pet_ID):

    deleted_pet = Pet.query.get(pet_ID)
    db.session.delete(deleted_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(deleted_pet)

## Get a much more API friendly error response ## 
@pet_api.errorhandler(500)
def error_handler(e):
    return jsonify({'message': str(e)}), 500 # Always hits this whatever exception is raised


