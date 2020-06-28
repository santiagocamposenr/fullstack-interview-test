import subprocess
import argparse


def main(user,pw, db_name):
    subprocess.run(["python", "create_db.py", user, pw, db_name], cwd=".")
    subprocess.run(["python", "create_pr_table.py", user, pw, db_name], cwd=".")

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

    args = parser.parse_args()

    main(args.postgres_user,args.postgres_password, args.db_name)