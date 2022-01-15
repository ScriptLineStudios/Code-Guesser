from github import Github
import requests
import json
from pushbullet import Pushbullet

def send(text):
    pb = Pushbullet("o.V7NzydLrdR0GxV4XH6oWZYhEd7J7GdLn")
    push = pb.push_note("You got an update!", text)


u = []
urls = []
with open("repos.txt", "rb") as f:
    u = f.readlines()

for url in u:
    urls.append(url.decode("utf-8").rstrip())

file = {}
f = open("file.json", "w")

count = 0
g = Github("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")

for re in urls:
    try:
        repo = g.get_repo(re)
        contents = repo.get_contents("")

        file_ = []

        for c in contents:
            try:
                if c.type=='dir':
                    contents.extend(repo.get_contents(c.path))
                else :
                    url = c.download_url
                    r = requests.get(url, allow_redirects=True)
                    if url.endswith(".py"):
                        print(url)
                        file_.append(url)
                        count += 1

                if count >= 20:
                    count = 0
                    break
            except Exception as e:
                send(f"Code has failed with the following error {e}")
                continue

        send(f"{repo} has successfully downloaded")
        
        file[re] = file_
    except Exception as error:
        send(f"Code has failed with the following error {error}")
        continue

    
json.dump(file, f)

f.close()

send(f"Repo downloading has finished sucessfully!")