from flask import Flask
from models import *
from config import config
from github import Github


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/github_db' # postgresql://<nombre_usuario>:<password>@<host>:<puerto>/<nombre_basededatos>
                                                                                 # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:testing@localhost:5432/miniblog'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# using username and password to connect with GitHub
user = config()['creds']['user']
password = config()['creds']['password']
g = Github(user, password)

# Fillling the DB
def main():
    for repo in g.get_user().get_repos():
        if repo.name == "fullstack-interview-test":
            branches = repo.get_branches()
    bases_list=[]
    for branch in branches:
        bases_list.append(branch.name)

    for base in bases_list:
        for repo in g.get_user().get_repos():
            if repo.name == "fullstack-interview-test":    
                pulls = repo.get_pulls(state='all', sort='created', base=base)
                for pr in pulls:
                    pr_ = Pullrequest(id=pr.id,author=pr.user.login,title=pr.title,description=pr.body,status=pr.state,base=pr.base.ref)
                    db.session.add(pr_)
                    print(f"Added PR with id {pr.id} author {pr.user.login} with title {pr.title} and description {pr.body}, state {pr.state}, base {pr.base.ref}")
        
    db.session.commit()

if __name__ == "__main__":
  with app.app_context():
    main()