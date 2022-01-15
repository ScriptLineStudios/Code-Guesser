from xml.dom import NamespaceErr
from github import Github
import requests
import random

def get_script() -> list:
  names = []
  g = Github("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")
  repo = g.get_repo("ScriptLineStudios/Contagious")
  contents = repo.get_contents("")
  while len(contents)>0:
    file_content = contents.pop(0)
    if file_content.type=='dir':
      contents.extend(repo.get_contents(file_content.path))
    else :
      url = file_content.download_url
      r = requests.get(url, allow_redirects=True)
      if url.endswith(".py"):
          string = url.split("/")[-1]
          print(url)
          names.append([f'{string}', r.content])
  return random.choice(names)

'''def get_script():
  return ["huewhuyefghwigyfv"]'''


