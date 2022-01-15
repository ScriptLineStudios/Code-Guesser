import random, json
from github import Github
g = Github("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")
u = []
urls = []
with open("repos.txt", "rb") as f:
    u = f.readlines()

for url in u:
    urls.append(url.decode("utf-8").rstrip())

choice = None

choice = random.choice(urls)
print(choice)
repo = g.get_repo(choice)
print(repo.description)

data = json.load(open("file.json"))
print(random.choice(data[choice]))

