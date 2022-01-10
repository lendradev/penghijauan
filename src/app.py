import os, sys, base64, traceback, random
from github import Github, GithubException
from github.InputGitAuthor import InputGitAuthor

ghtoken=os.getenv("INPUT_GH_TOKEN")
repository=os.getenv("INPUT_REPOSITORY")
branch=os.getenv("INPUT_BRANCH")
username=os.getenv("INPUT_USERNAME")
email=os.getenv("INPUT_EMAIL")

def generateRandomId(length: int):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(characters) for i in range(length))

def decodeContent(data: str):
    byte_decodes = base64.b64decode(data)
    return str(byte_decodes, "utf-8")

def getCommitbyProgram(info: str):
    totalCommit = 1
    for line in info:
        if line != "\n":
            totalCommit += 1
    
    return totalCommit

def generateInfo():
    return f"{generateRandomId(length=20)}"

def main():
    try:    
        gh = Github(ghtoken)
        try:
            repo = gh.get_repo(repository)
        except GithubException:
            print("Error: gagal mendapatkan repository")
            sys.exit(1)

        content = repo.get_contents("info")
        totalCommit = repo.get_commits().totalCount + 1
        newInfo = generateInfo()
        commitMessage = f"Commit #{totalCommit}"
        committer = InputGitAuthor(username, email)

        try: 
            repo.update_file(path=content.path, message=commitMessage, content=newInfo, 
                sha=content.sha, branch=branch, committer=committer)
        except Exception as error:
            traceback.print_exc()
            print(f"Exception occured: {str(error)}")

        print("Info updated")
    except Exception as e:
        traceback.print_exc()
        print(f"Exception occured: {str(e)}")

if __name__ == "__main__":
    main()