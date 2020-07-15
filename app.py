from flask import Flask, render_template, abort,session,redirect,url_for
from forms import LoginForm, SignupForm, AdoptationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Paws__Center.db'
db = SQLAlchemy(app)


"""Model for Pets."""
class Pet(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    age  = db.Column(db.String, nullable=False)
    bio  = db.Column(db.String, nullable=False)
    adopted  = db.Column(db.Boolean, nullable=False)
    #create a forgien key from Users class
    adopted_by = db.Column(db.String, db.ForeignKey('user.id'))

"""Model for Users."""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    #set one-to-many relationship between users and pets
    #This back-reference will enable us to point to a row in User by using pet.user.
    pets = db.relationship('Pet', backref = 'user')

db.create_all()



# Create all pets
nelly  = Pet(name = "Nelly",  age = "5 weeks",  bio = "I'm Nelly, I love squeaky toys and cuddles.", adopted=False)
yuki   = Pet(name = "Yuki",   age = "8 months", bio = "I'm handsome cat like to dress up in bow ties",adopted=False)
basker = Pet(name = "Basker", age = "1 year",   bio = "I love barking. But, I love my friends more.",adopted=False)
mrfurrkins = Pet(name = "Mr. Furrkins", age = "5 years", bio = "Hi! I'm an old grandpa, Probably napping!",adopted=False)
Aze    = Pet(name = "Aze",   age = "1 year",  bio = "I'm a quite cat, i love treats.",adopted=False)
suna   = Pet(name = "suna",  age = "2 month", bio = "Hi! I'm an old grandpa, Probably napping!",adopted=False)
Natcha = Pet(name = "Natcha",age = "4 year",  bio = "........................",adopted=False)
Buny   = Pet(name = "Buny",  age = "3 month", bio = "........................",adopted=False)

# Add all pets to the session
db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mrfurrkins)
db.session.add(Aze)
db.session.add(suna)
db.session.add(Natcha)
db.session.add(Buny)


# Commit changes in the session
try:
    db.session.commit()
except Exception as e: 
    db.session.rollback()
finally:
    db.session.close()


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


          
if __name__ == "__main__":
    app.run(debug=True)