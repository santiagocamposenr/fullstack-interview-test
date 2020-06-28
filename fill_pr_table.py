from flask import Flask
from models import *
from github import Github
import argparse
from get_repo import get_repo


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

parser.add_argument("github_user",
                    help="This is your username in GitHub",
                    type=str)

parser.add_argument("github_password",
                    help="This is your password in GitHub",
                    type=str)

args = parser.parse_args()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{args.postgres_user}:{args.postgres_password}@localhost:5432/{args.db_name}" # postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# using username and password to connect with GitHub
user = args.github_user
password = args.github_password
g = Github(user, password)

# Fillling the DB
def main():
    repo = get_repo(g)
    for branch in repo.get_branches():
        base = branch.name
        pulls = repo.get_pulls(state='all', sort='created', base=base)
        for pr in pulls:
            pr_ = Pullrequest(id=pr.id,author=pr.user.login,title=pr.title,description=pr.body,status=pr.state,base=pr.base.ref)
            db.session.add(pr_)
            print(f"Added PR with id {pr.id} author {pr.user.login} with title {pr.title} and description {pr.body}, state {pr.state}, base {pr.base.ref}")
    db.session.commit()

if __name__ == "__main__":
  with app.app_context():
    main()