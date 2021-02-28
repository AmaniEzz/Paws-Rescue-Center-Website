from flask import Flask
from flask_migrate import Migrate
from admin import setup_admin
from models import db
from API_views import pet_api
from website_views import site

app = Flask(__name__)

# register blueprints
app.register_blueprint(pet_api)
app.register_blueprint(site)

# config database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Paws__Center.db'

# handles SQLAlchemy database migrations
db.init_app(app)
MIGRATE = Migrate(app, db)

# setup admin interface
setup_admin(app)

if __name__ == "__main__":
    app.run(debug=True)