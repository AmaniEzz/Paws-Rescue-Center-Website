from flask import Flask, render_template, abort,session,redirect,url_for, jsonify
from forms import LoginForm, SignupForm, AdoptationForm
from flask import make_response
from flask import request
from admin import setup_admin
from models import db, User, Pet, PetSchema, UserSchema

from flask import Blueprint

site = Blueprint('site', __name__)


@site.route("/")
def home():
    return render_template("home.html", pets= Pet.query.filter(Pet.adopted==False))

@site.route("/about")
def about():
    return render_template("about.html")

@site.route("/signup", methods=["GET", "POST"])
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


@site.route("/login", methods=["GET", "POST"])
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


@site.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('home'))


@site.route("/contact")
def contact():
    return render_template("contact.html")


@site.route("/details/<int:pet_ID>", methods=["GET", "POST"])
def pet_details(pet_ID):
    form = AdoptationForm()
    pet = Pet.query.get(pet_ID)
    if pet is not None:
        if form.validate_on_submit():
            return render_template("details.html", msg= "Successfully submited adoptation request")
    else:
           abort(404, description="No pet found with this ID")
    return render_template("details.html", form = form,  pet = pet, pet_ID=pet_ID)


@site.errorhandler(500)
def error_handler(e):
    return jsonify({'message': str(e)}), 500 # Always hits this whatever exception is raised
