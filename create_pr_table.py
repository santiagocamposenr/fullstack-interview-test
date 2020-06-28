from flask import Flask
from models import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("postgres_user",
                    help="This is your username in Postgres",
                    type=str)

parser.add_argument("postgres_password",
                    help="This is your password in Postgres",
                    type=str)

parser.add_argument("db_name",
                    help="This is how you want to name the db",
                    type=str)

args = parser.parse_args()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{args.postgres_user}:{args.postgres_password}@localhost:5432/{args.db_name}" # postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if __name__ == "__main__":
  with app.app_context():
    # Creating the bd
    db.create_all()
