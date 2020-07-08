from flask import Flask, render_template, abort
from forms import LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

"""Information regarding the Pets in the System."""
pets = [
    {"id": 1, "name": "Nelly", "age": "5 weeks",        "bio": "I love squeaky toys and cuddles......."},
    {"id": 2, "name": "Yuki", "age": "8 months",        "bio": "I'm handsome cat like to dress up in bow ties."},
    {"id": 3, "name": "Basker", "age": "1 year",        "bio": "I love barking. But, I love my friends more..."},
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "I'm an old grandpa, Probably napping.........."}, 
    {"id": 5, "name": "Aze", "age": "1 year",           "bio": "I'm a quite cat, i love treats."},
    {"id": 6, "name": "suna", "age": "2 month",         "bio": "I feel so lucky to be rescued."},
    {"id": 5, "name": "Aze", "age": "1 year",           "bio": "I'm a quite cat, i love treats."},
    {"id": 6, "name": "suna", "age": "2 month",         "bio": "i feel so lucky to be rescued."},

    ]

users = {
    "archie.andrews@email.com": "football4life",
    "veronica.lodge@email.com": "fashiondiva"
}
    
@app.route("/")
def home():
    return render_template("home.html", pets=pets)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
   
    if form.validate_on_submit():
       print("Submitted and Valid.")

    elif form.errors:
        print(form.errors.items())

    return render_template("login.html", form = form)


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
    app.run(debug=True, port=4000)