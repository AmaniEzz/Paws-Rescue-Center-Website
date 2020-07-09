from flask import Flask, render_template, abort,session,redirect,url_for
from forms import LoginForm, SignupForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'


"""Information regarding the Pets in the System."""
pets = [
    {"id": 1, "name": "Nelly", "age": "5 weeks",        "bio": "I'm Nelly, I love squeaky toys and cuddles."},
    {"id": 2, "name": "Yuki", "age": "8 months",        "bio": "I'm handsome cat like to dress up in bow ties."},
    {"id": 3, "name": "Basker", "age": "1 year",        "bio": "I love barking. But, I love my friends more."},
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Hi! I'm an old grandpa, Probably napping!"}, 
    {"id": 5, "name": "Aze", "age": "1 year",           "bio": "I'm a quite cat, i love treats."},
    {"id": 6, "name": "suna", "age": "2 month",         "bio": "I feel so lucky to be rescued."},
    {"id": 5, "name": "Aze", "age": "1 year",           "bio": "I'm a quite cat, i love treats."},
    {"id": 6, "name": "suna", "age": "2 month",         "bio": "i feel so lucky to be rescued."},

    ]

"""Information regarding the Users in the System."""

users = [
    {"username": "Amany", "password":"ddddddd", "email": "amanymounas@gmail.com"},
    {"username": "Mona",  "password":"4534366", "email": "Mona.M@email.com"},
    {"username": "Ahmed", "password":"deh3nb4", "email": "Ahmed1234@gmail.com"},
    {"username": "Magdy", "password":"uud7dye", "email": "Magdy1234@gmail.com"},
   
]
print(users)

@app.route("/")
def home():
    return render_template("home.html", pets=pets)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = {"username": form.username.data, "password": form.password.data, "email": form.email.data}
        users.append(new_user)
        return render_template("signup.html",  message = "Successfully Signed up")

    return render_template("signup.html", form =form, email_error = form.email.errors, confirm_error =form.confirm.errors)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        for user in users:
            user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
            if user is None:
                return render_template("login.html", form = form, msg= "Wrong Credentials.")

            else:
                session['user'] = user
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


@app.route("/details/<int:pet_ID>")
def pet_details(pet_ID):
    exists = False
    for pet in pets:
       if pet_ID == pet["id"]:
          exists = True
          return render_template("details.html", pet = pet)
       
    if exists == False:
       abort(404, description="No pet found with this ID")


if __name__ == "__main__":
    app.run(debug=True, port=6162)