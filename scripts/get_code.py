import random, json
from github import Github
from scripts.config import API_KEY

g = Github(API_KEY)
u = []
urls = []
with open("data/repos.txt", "rb") as f:
    u = f.readlines()

for url in u:
    urls.append(url.decode("utf-8").rstrip())


def get_repo():
    choice = None

    choice = random.choice(urls)
    repo = g.get_repo(choice)
    repo_description = repo.description

    data = json.load(open("data/file.json"))
    script = random.choice(data[choice])

    return repo_description, script

def get_random_desc():
    choice = None

    choice = random.choice(urls)
    repo = g.get_repo(choice)
    repo_description = repo.description

    return repo_description

