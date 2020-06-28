from flask import Flask, render_template, jsonify, request, make_response
from git import Repo
from github import Github
import requests
from config import config
import re
import os
from models import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost:5432/github_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# using username and password to connect with GitHub
user = config()['creds']['user']
password = config()['creds']['password']
g = Github(user, password)

# Connect with the cloned repo
repo_path = os.getenv('GIT_REPO_PATH')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pullrequests")
def pullrequests():
    """List all Pull requests."""
    url = "http://127.0.0.1:5000/api/pullrequests"
    r = requests.get(url = url)
    # extracting data in json format 
    json_response = r.json()
    pull_requests = json_response['results']
    return render_template("pull_requests.html", pull_requests=pull_requests)

@app.route("/close_pullrequest", methods=["POST"])
def close_pullrequest():
    """Close a Pull request"""
    # Get form information.
    pr_title = request.form.get("pr_title")
    pr_base = request.form.get("pr_base")
    pr_id = 0
    # Create the PR
    for repo in g.get_user().get_repos():
        if repo.name == "fullstack-interview-test":
            pulls = repo.get_pulls(state='open', sort='created', base=pr_base)
            for pr in pulls:
                if pr.title == pr_title:
                    pr_id = pr.id
                    pr.edit(state="closed")

    # Updating the state in th db
    pull_request = Pullrequest.query.get(pr_id)
    pull_request.status = "closed"
    db.session.commit()
    return render_template("success.html", pr_title=pr_title) 
   
@app.route("/pullrequest_form")
def pullrequest_form():
    """Create a Pull request"""
    return render_template("pullrequest_form.html")

@app.route("/create_pullrequest", methods=["POST"])
def create_pullrequest():
    """Create a Pull request"""
    base = request.form.get("base")
    compare = request.form.get("compare")
    pr_title = request.form.get("pr_title")
    pr_body = request.form.get("pr_body")
    status = request.form.get("status")

    # Create the PR
    for repo in g.get_user().get_repos():
        if repo.name == "fullstack-interview-test":
            pr = repo.create_pull(title=pr_title, body=pr_body
            , head=compare, base=base)
            # pr = repo.get_pull(3)
            if status == "merge":
                try:
                    response = pr.merge()
                    return "Successfull Merge"
                except Exception as e:
                    # e.data.message
                    return render_template("error.html", message="Ocurrio un error")
    return "Pull Request created"

@app.route("/branches")
def branches():
    """List all branches."""
    url = "http://127.0.0.1:5000/api/branches"
    r = requests.get(url = url)
    # extracting data in json format 
    json_response = r.json()
    branches = json_response['results']
    return render_template("branches.html", branches=branches)

@app.route("/branches/<branch_id>")
def branch(branch_id):
    """List details about a single branch."""
    branch_id=branch_id
    url = "http://127.0.0.1:5000/api/branches/{}".format(branch_id)
    r = requests.get(url = url)
    # extracting data in json format 
    json_response = r.json()
    commits = json_response['results']
    return render_template("branch.html", commits=commits)

@app.route("/branches/<branch_id>/commits/<commit_id>")
def commit(branch_id,commit_id):
    """List details about a single commit."""
    branch_id=branch_id
    commit_id=commit_id
    url = "http://127.0.0.1:5000/api/branches/{}".format(branch_id)
    r = requests.get(url = url)
    # extracting data in json format 
    json_response = r.json()
    commits = json_response['results']
    for commit in commits:
        if commit_id == commit["id"]:
            return render_template("commit.html", commit=commit)

@app.route("/api/pullrequests")
def pullrequests_api():
    """ Return the list of pullrequests """

    # Getting the new PRs
    for repo in g.get_user().get_repos():
        if repo.name == "fullstack-interview-test":
            branches = repo.get_branches()
    bases_list=[]
    for branch in branches:
        bases_list.append(branch.name)
    
    ids_in_db = {}
    pullrequests = Pullrequest.query.all()
    for pr in pullrequests:
        ids_in_db[pr.id] = pr.status
    

    for base in bases_list:
        for repo in g.get_user().get_repos():
            if repo.name == "fullstack-interview-test":    
                pulls = repo.get_pulls(state='all', sort='created', base=base)
                for pr in pulls:
                    if not pr.id in ids_in_db:
                        pr_ = Pullrequest(id=pr.id,author=pr.user.login,title=pr.title,description=pr.body,status=pr.state,base=pr.base.ref)
                        db.session.add(pr_)
                        print(f"Added PR with id {pr.id} author {pr.user.login} with title {pr.title} and description {pr.body}, state {pr.state}, base {pr.base.ref}")
                    else:
                        if ids_in_db[pr.id] != pr.state:
                            # Updating the state in th db
                            pull_request = Pullrequest.query.get(pr.id)
                            pull_request.status = pr.state
                        else:
                            pass

    pullrequests = Pullrequest.query.all()
    if pullrequests is None:
        return jsonify({"error": "There is not pull requests"}), 422
    pullrequests_list= [] 

    for pr in pullrequests:
        pr_obj={}
        pr_obj["id"]=pr.id
        pr_obj["author"]=pr.author
        pr_obj["title"]=pr.title
        pr_obj["description"]=pr.description
        pr_obj["status"]=pr.status
        pr_obj["base"]=pr.base
        pullrequests_list.append(pr_obj)
    
    response = make_response(jsonify(results=pullrequests_list))
    response.headers['Access-Control-Allow-Origin']='*'   
    return response #jsonify(results=commits_list)

@app.route("/api/branches")
def branches_api():
    """ Return the list of branches """
    for repo in g.get_user().get_repos():
        if repo.name == "fullstack-interview-test":
            branches = repo.get_branches()

    if branches is None:
        return jsonify({"error": "There is not branches"}), 422
    branches_list= [] 

    for branch in branches:
        branch_obj={}
        branch_obj["id"]=branch.name
        branches_list.append(branch_obj)
    
    response = make_response(jsonify(results=branches_list))
    response.headers['Access-Control-Allow-Origin']='*'   
    return response 

@app.route("/api/branches/<branch_id>")
def branch_api(branch_id):
    """List details about a single branch."""
    
    # Repo object used to programmatically interact with Git repositories
    repo = Repo(repo_path)
    commits_list= [] 
    # check that the repository loaded correctly
    if not repo.bare:
        branches = list(repo.heads)
        for branch in branches:
            if branch_id == branch.name:
                commits = list(repo.iter_commits(branch.name))
                for commit in commits:               
                    commit_obj={}
                    commit_obj["id"]=str(commit.hexsha)
                    commit_obj["message"]=commit.summary
                    commit_obj["timestamp"]=commit.authored_datetime
                    commit_obj["name"]=commit.author.name
                    commit_obj["email"]=commit.author.email
                    commit_obj["branch_id"]=branch.name
                    # Getting the numer of files changed
                    repo_to_get_files = g.get_user().get_repo(name="fullstack-interview-test")
                    commit_to_get_files = repo_to_get_files.get_commit(sha=commit.hexsha)
                    commit_obj["files_changed"]=len(commit_to_get_files.files)
                    commits_list.append(commit_obj)
    
    response = make_response(jsonify(results=commits_list))
    response.headers['Access-Control-Allow-Origin']='*'   
    return response #jsonify(results=commits_list)
