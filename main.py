import argparse
import subprocess

def main(postgres_user, postgres_password, db_name, github_user, github_password):
    print("Filling the db")
    subprocess.run(["python", "fill_pr_table.py", postgres_user, postgres_password, db_name, github_user, github_password], cwd=".")
    subprocess.run(["python", "application.py", postgres_user, postgres_password, db_name, github_user, github_password], cwd=".")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("postgres_user",
                        help="This is your username in Postgres",
                        type=str)

    parser.add_argument("postgres_password",
                        help="This is your password in Postgres",
                        type=str)

    parser.add_argument("db_name",
                        help="This is how you named your db when running make_db_schema.py",
                        type=str)

    parser.add_argument("github_user",
                        help="This is your username in GitHub",
                        type=str)

    parser.add_argument("github_password",
                        help="This is your password in GitHub",
                        type=str)

    args = parser.parse_args()

    main(args.postgres_user,args.postgres_password, args.db_name, args.github_user, args.github_password)