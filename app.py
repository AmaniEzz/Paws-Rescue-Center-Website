from flask import Flask, render_template, abort,session,redirect,url_for, jsonify
from forms import LoginForm, SignupForm, AdoptationForm
from flask_sqlalchemy import SQLAlchemy
from flask import make_response
from flask import request
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
import os
from admin import setup_admin
from models import db, User, Pet, PetSchema, UserSchema

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Paws__Center.db'

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


##################################################################################################################
############################################## Application routes ################################################

@app.route("/")
def home():
    return render_template("home.html", pets= Pet.query.filter(Pet.adopted==False))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username= form.username.data, password= form.password.data, email= form.email.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e: 
            db.session.rollback()
            return render_template("signup.html", 
            form = form, message = "This Email already exists in the system! Please Log in instead.")
        finally:
            db.session.close()  

        return render_template("signup.html",  message = "Successfully Signed up")

    return render_template("signup.html", form =form, email_error = form.email.errors, 
    confirm_error =form.confirm.errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, msg= "Wrong Credentials.")

        else:
            session['user'] = user.id
            return render_template("user_page.html", msg= "Successfully Logged In")

    return render_template("login.html", form = form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/details/<int:pet_ID>", methods=["GET", "POST"])
def pet_details(pet_ID):
    form = AdoptationForm()
    pet = Pet.query.get(pet_ID)
    if pet is not None:
        if form.validate_on_submit():
            return render_template("details.html", msg= "Successfully submited adoptation request")
    else:
           abort(404, description="No pet found with this ID")
    return render_template("details.html", form = form,  pet = pet, pet_ID=pet_ID)

          
############################################################################
############################ API Routes ####################################


@app.route("/pets/api/v1.0/pets", methods=['GET'])
def get_all():
    All_Pets =  Pet.query.all()
    
    # Serialize all data for the response
    Pet_schema = PetSchema(many=True)
    return jsonify(Pet_schema.dump(All_Pets))


@app.route('/pets/api/v1.0/details/<int:pet_ID>', methods=['GET'])
def get_a_pet(pet_ID):
    pet = Pet.query.get(pet_ID)

    if pet is not None:
        Pet_schema = PetSchema()
        return Pet_schema.dump(pet)
    else:
        abort(404, 'Pet not found for Id: {pet_ID}'.format(pet_ID=pet_ID))


@app.route('/pets/api/v1.0/create', methods=['POST'])
def Newpet():
       name = request.json.get('name', '')
       age = request.json.get('age', '')
       bio = request.json.get('bio', '')
       
       new_pet = Pet(name = name, age=age, bio=bio)
       
       db.session.add(new_pet)
       db.session.commit()

       Pet_schema = PetSchema()
       return Pet_schema.dump(new_pet)

################################### [PATCH] updating pets info ###########################################

@app.route('/pets/api/v1.0/update_all/<int:pet_ID>/', methods=['PATCH'])
def update_pet_info(pet_ID):
    name = request.json.get('name', '')
    age  = request.get('ages', '')
    bio  = request.get('bio', '')
    updated_pet = Pet.query.get(pet_ID)

    updated_pet.name = name
    updated_pet.age = age
    updated_pet.bio = bio

    db.session.add(updated_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(updated_pet)

@app.route('/pets/api/v1.0/update_name/<int:pet_ID>/', methods=['PATCH'])
def update_pet_name(pet_ID):
    name = request.json.get('name', '')
    updated_pet = Pet.query.get(pet_ID)

    updated_pet.name = name
    db.session.add(updated_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(updated_pet)

@app.route('/pets/api/v1.0/update_age/<int:pet_ID>/', methods=['PATCH'])
def update_pet_age(pet_ID):
    age = request.json.get('age', '')
    updated_pet = Pet.query.get(pet_ID)
    updated_pet.age = age
    db.session.add(updated_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(updated_pet)

@app.route('/pets/api/v1.0/update_bio/<int:pet_ID>/', methods=['PATCH'])
def update_pet_bio(pet_ID):
    bio  = request.get('bio', '')
    updated_pet = Pet.query.get(pet_ID)
    updated_pet.bio = bio
    db.session.add(updated_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(updated_pet)

########################################################################################################

@app.route('/pets/api/v1.0/delete/<int:pet_ID>/', methods=["DELETE"])
def delete_pet(pet_ID):

    deleted_pet = Pet.query.get(pet_ID)
    db.session.delete(deleted_pet)
    db.session.commit()

    Pet_schema = PetSchema()
    return Pet_schema.dump(deleted_pet)


## Get a much more API friendly error response ## 
@app.errorhandler(500)
def error_handler(e):
    return jsonify({'message': str(e)}), 500 # Always hits this whatever exception is raised


if __name__ == "__main__":
    app.run(debug=True)