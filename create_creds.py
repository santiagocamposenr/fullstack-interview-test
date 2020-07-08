import os
import argparse
import json
import subprocess


def make_creds_file(postgres_user, postgres_password, db_name, github_user, github_password):
    if os.path.isfile('./config.json'):
        print('config file already exist')
    else:
        data = {'postgres_user': postgres_user, 'postgres_password': postgres_password,
                'db_name': db_name, 'github_user': github_user, 'github_password': github_password}
        with open('config.json', mode='w+') as outfile:
            json.dump(data, outfile)
        print('config file was created')


def read_creds_file():
    with open('config.json', mode='r') as json_file:
        data = json.load(json_file)
        config = {}
        config['postgres_user'] = data['postgres_user']
        config['postgres_password'] = data['postgres_password']
        config['db_name'] = data['db_name']
        config['github_user'] = data['github_user']
        config['github_password'] = data['github_password']

        return config


if __name__ == "__main__":
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

    make_creds_file(args.postgres_user, args.postgres_password,
                    args.db_name, args.github_user, args.github_password)
