import os
from flask_admin import Admin
from models import db, User, Pet
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Pet Rescue centre', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Pet, db.session))