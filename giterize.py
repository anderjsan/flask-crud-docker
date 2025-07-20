import os
import subprocess
import sys

def git_init_commit_push(username, repo_name):
    try:
        # Initialize a Git repository
        print("")
        subprocess.run(["git", "init"])

        # Remove the origin repository
        print("")
        subprocess.run(["git", "remote", "remove", "origin"])

        # Add the GitHub remote repository
        print("")
        github_url = f"https://github.com/{username}/{repo_name}.git"
        subprocess.run(["git", "remote", "add", "origin", github_url])

        # Add all files to the repository
        print("")
        subprocess.run(["git", "add", "."])

        # Make the first commit
        print("")
        commit_message = "[INIT] Very First Commit for " + repo_name
        subprocess.run(["git", "commit", "-m", commit_message])

        # Make an initial pull
        print("")
        subprocess.run(["git", "pull", "--set-upstream", "origin", "master", "--force"])
        
        # Make the initial push
        print("")
        subprocess.run(["git", "push", "--set-upstream", "origin", "master", "--force"])

        # End of process
        print("")
        print("Repository created on GitHub and files sent!")
    except Exception as e:
        print("")
        print("An error occurred:", e)
        

if __name__ == "__main__":
    # Check if the arguments are correct
    if len(sys.argv) != 3:
        print("Usage: python3 giterize.py [repository-name] [username]")
        sys.exit(1)

    # Get command line arguments
    username = sys.argv[1]
    repo_name = sys.argv[2]
    

    # Call the function to initialize the repository
    git_init_commit_push(username, repo_name)