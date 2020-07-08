import subprocess


def main():
    print("Filling the PullRequest table")
    subprocess.run(["python", "fill_pr_table.py"], cwd=".")
    subprocess.run(["python", "application.py"], cwd=".")


if __name__ == "__main__":
    main()
