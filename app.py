from flask import Flask, render_template, request, session
import requests
from get_code import get_repo, get_random_desc
import random
import pickle

app = Flask(__name__)

games = []
pickle.dump(games, open("json.pickle", "wb"))


def generate_round(): 
    desc, code = get_repo()
    r = requests.get(code, allow_redirects=True)
    file = open(code.strip("/")[-1], 'wb').write(r.content)
    b_lines = []
    with open(code.strip("/")[-1], 'rb') as f:
        for row in f:
            b_lines.append(row.decode('utf-8').rstrip())

    if b_lines == []:
        generate_round()
    else:
        return b_lines, desc


app.secret_key = "23piojf0wojhfwiuhgfieh5uytger[p9ouhg"
@app.route("/")
def menu():
    return render_template('menu.html')   

@app.route("/play")
def play():

    b_lines, desc = generate_round()


    repo_decsriptions = [[desc, "c"], [get_random_desc(), "i"], [get_random_desc(), "i"], [get_random_desc(), "i"]]

    repos = []

    for x in range(4):
        choice = random.choice(repo_decsriptions)
        repos.append(choice)
        repo_decsriptions.remove(choice)

    games = pickle.load(open("json.pickle", "rb"))
    games.append(repos)
    index = games.index(games[-1])
    pickle.dump(games, open("json.pickle", "wb"))

    return render_template('play.html', b_lines=b_lines, repo_1=repos[0][0], repo_2 =repos[1][0], repo_3 =repos[2][0], repo_4 =repos[3][0], index=index, repo_dsc=repo_decsriptions)   

@app.route('/result',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      index = request.form['index']
      guess = request.form['guess']
      games = pickle.load(open("json.pickle", "rb"))

        
      if games[int(index)][int(guess)][1] == "c" and int(guess) > -1:
          return render_template("correct.html")
      else: 
        return render_template("incorrect.html")
   else:
      return "None"


if __name__ == "__main__":
    app.run(debug=True, host="localhost")