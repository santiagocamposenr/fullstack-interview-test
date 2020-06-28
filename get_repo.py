from github import Github

def get_repo(g):
    for repo in g.get_user().get_repos():
        if repo.name == "fullstack-interview-test":
            return repo