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

def main():
    ids = []
    prs=Pullrequest.query.all()
    for pr in prs:
        ids.append(pr.id)
    print(ids)

if __name__ == "__main__":
  with app.app_context():
    main()