# fullstack-interview-test

## Requirements

### 1. Flask
```
    pip install flask
```
### 2. Flask-SQLAlchemy
```
    pip install Flask-SQLAlchemy
```
### 3. Psycopg2-binary
```
    pip install psycopg2-binary
```
### 4. PyGithub
```
    pip install PyGithub
```
### 5. GitPython
```
    pip install gitpython
```
### 6. Requests
```
    pip install requests
```
### 7. Postgres
Postgres is needed.

[How to install Postgres](https://www.digitalocean.com/community/tutorials/como-instalar-y-utilizar-postgresql-en-ubuntu-18-04-es)

### 8. Clone the repository to use GitPython

Clone a repository you want to work with to your local system.
Use the export command to set an environment variable for the absolute path to the Git repository.
```
export GIT_REPO_PATH='/home/santiago/Documents/fullstack-interview-test'
```

## Run the code

### 1. Create the db schema

First you have to create the db, to do that run in terminal the file make_db_schema.py.

This command needs 3 positional arguments:
* postgres_user      This is your username in Postgres
* postgres_password  This is your password in Postgres
* db_name            This is how you want to name the db

Example:
```
python make_db_schema.py postgres_user postgres_password db_name
```

You can use the _python make_db_schema.py -h_ to get help.

### 2. Run the project

Once you have the db, run the command python main.py.

This command needs 5 positional arguments:
* postgres_user      This is your username in Postgres
* postgres_password  This is your password in Postgres
* db_name            This is how you want to name the db
* github_user        This is your username in GitHub
* github_password    This is your password in GitHub

Example:
```
python main.py postgres_user postgres_password db_name github_user github_password
```

You can use the _python main.py -h_ to get help.

## Limitations
Currently the code will work only with the repository "fullstack-interview-test". 
The repository must exist in the user account that inserts their credentials to execute the code

