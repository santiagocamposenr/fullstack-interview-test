from flask import Flask
from models import *
from create_creds import read_creds_file

creds = read_creds_file()

app = Flask(__name__)
# postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{creds['postgres_user']}:{creds['postgres_password']}@localhost:5432/{creds['db_name']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        # Creating the bd
        db.create_all()
