# fullstack-interview-test

## Requirements

### 1. Run

```
    pip install -r requirements.txt
```

### 2. Postgres

Postgres is needed.

[How to install Postgres](https://www.digitalocean.com/community/tutorials/como-instalar-y-utilizar-postgresql-en-ubuntu-18-04-es)

### 3. Clone the repository to use GitPython

Clone a repository you want to work with to your local system.
Use the export command to set an environment variable for the absolute path to the Git repository.

```

export GIT_REPO_PATH='/home/santiago/Documents/fullstack-interview-test'

```

## Run the code

### 1. Create credentials for the project

First you have to create the credentials for this project, run the command python create_creds.py.

This command needs 5 positional arguments:

- postgres_user This is your username in Postgres
- postgres_password This is your password in Postgres
- db_name This is how you want to name the db
- github_user This is your username in GitHub
- github_password This is your password in GitHub

Example:

```

python create_creds.py postgres_user postgres_password db_name github_user github_password

```

You can use the _python main.py -h_ to get help.

### 2. Create the db schema

Now you have to create the db, to do that run in terminal the file make_db_schema.py.

Example:

```

python make_db_schema.py

```

### 3. Run the project

Once you have the db, run the command python main.py.

Example:

```

python main.py

```
