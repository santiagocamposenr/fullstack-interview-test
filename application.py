from flask import Flask, render_template, jsonify, make_response
from git import Repo
from github import Github
import requests
from config import config
import re
import os

# using username and password to connect with GitHub
user = config()['creds']['user']
password = config()['creds']['password']
g = Github(user, password)

# Connect with the cloned repo
repo_path = os.getenv('GIT_REPO_PATH')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/branches")
def branches():
    """List all branches."""
    url = "http://127.0.0.1:5000/api/branches"
    r = requests.get(url = url)
    # extracting data in json format 
    json_response = r.json()
    branches = json_response['results']
    return render_template("branches.html", branches=branches)

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
    
