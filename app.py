from flask import Flask, render_template, request
from scripts.get_code import get_random_desc
import random
import pickle
from scripts.generate_round import generate_round
from scripts.config import SECRECT_KEY

app = Flask(__name__)

games = []
pickle.dump(games, open("data/json.pickle", "wb"))

app.secret_key = SECRECT_KEY

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

    games = pickle.load(open("data/json.pickle", "rb"))
    games.append(repos)
    index = games.index(games[-1])
    pickle.dump(games, open("data/json.pickle", "wb"))

    return render_template('play.html', b_lines=b_lines, repo_1=repos[0][0], repo_2 =repos[1][0], repo_3 =repos[2][0], repo_4 =repos[3][0], index=index, repo_dsc=repo_decsriptions)   

@app.route('/result',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      index = request.form['index']
      guess = request.form['guess']
      games = pickle.load(open("data/json.pickle", "rb"))

      if games[int(index)][int(guess)][1] == "c" and int(guess) > -1:
          return render_template("correct.html")
      else: 
        return render_template("incorrect.html")
   else:
      return "None"


if __name__ == "__main__":
    app.run(debug=True, host="localhost")