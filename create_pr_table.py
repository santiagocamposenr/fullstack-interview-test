from flask import Flask
from models import *
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/github_db' # postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
                                                                                 # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
# Creating the bd
def main():
    db.create_all()

if __name__ == "__main__":
  with app.app_context():
    main()