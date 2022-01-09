from functools import total_ordering
import os, sys, base64, re
from github import Github, GithubException
from github.InputGitAuthor import InputGitAuthor

ghtoken=os.getenv("INPUT_GH_TOKEN")
repository=os.getenv("INPUT_REPOSITORY")
branch=os.getenv("INPUT_BRANCH")
username=os.getenv("INPUT_USERNAME")
email=os.getenv("INPUT_EMAIL")

def decodeContent(data: str):
    byte_decodes = base64.b64decode(data)
    return str(byte_decodes, "utf-8")

def getCommitbyProgram(info: str):
    totalCommit = 1
    for line in info:
        if line != "\n":
            totalCommit += 1
    
    return totalCommit

def generateInfo(oldInfo: str):
    totalCommit = 1
    for line in oldInfo:
        if line != "\n":
            totalCommit += 1

    textInfo = f"Commit yang dibuat oleh program ini ke #{totalCommit} kali\n"
    return f"{oldInfo}\n{textInfo}"


def main():
    gh = Github(ghtoken)
    try:
        repo = gh.get_repo(repository)
    except GithubException:
        print("Tidak dapat menemukan repository")
        sys.exit(1)
    
    content = repo.get_contents("./info")
    oldInfo = decodeContent(content.content)
    newInfo = generateInfo(oldInfo)
    user = gh.get_user()
    commitMessage = f"Commit yang dibuat oleh program ini ke #{getCommitbyProgram(oldInfo)} kali\n"
    committer = InputGitAuthor(user.name, user.email)
    if newInfo != oldInfo:
        repo.update_file(path=content.path, message=commitMessage, content=newInfo, 
            sha=content.sha, branch=branch, committer=committer, 
        )
        print("Info updated")

if __name__ == "__main__":
    main()