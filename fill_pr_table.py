from flask import Flask
from models import *
from github import Github
from get_repo import get_repo
from create_creds import read_creds_file


creds = read_creds_file()

app = Flask(__name__)
# postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{creds['postgres_user']}:{creds['postgres_password']}@localhost:5432/{creds['db_name']}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# using username and password to connect with GitHub
user = creds['github_user']
password = creds['github_password']
g = Github(user, password)

# Fillling the DB


def main():
    repo = get_repo(g)
    for branch in repo.get_branches():
        base = branch.name
        pulls = repo.get_pulls(state='all', sort='created', base=base)
        for pr in pulls:
            pr_ = Pullrequest(id=pr.id, author=pr.user.login, title=pr.title,
                              description=pr.body, status=pr.state, base=pr.base.ref)
            db.session.add(pr_)
            print(
                f"Added PR with id {pr.id} author {pr.user.login} with title {pr.title} and description {pr.body}, state {pr.state}, base {pr.base.ref}")
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
