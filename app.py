from flask import Flask, render_template, request, redirect, url_for, make_response, session
from scripts.get_code import get_random_desc
import random
import pickle
from scripts.generate_round import generate_round
from scripts.config import SECRECT_KEY
from authlib.integrations.flask_client import OAuth
from flask_github import GitHub
#from flask.ext.session import Session


app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config.from_object(__name__)
#Session(app)

games = []
pickle.dump(games, open("data/json.pickle", "wb"))

app.secret_key = SECRECT_KEY

@app.route("/")
def menu():
    session.clear()
    return render_template('menu.html')   

@app.route("/start")
def start():
    session["round_number"] = 0
    return redirect("/play/0")

@app.route("/new_round")
def new_round():
    session["round_number"] += 1
    return redirect(f"/play/{session['round_number']}")

@app.route("/play/<round_number>")
def play(round_number):
    real_round_number = str(session["round_number"])
    
    if round_number != real_round_number:
        return redirect(f"/play/{real_round_number}")
    if round_number in session:
        b_lines, repos, index, repo_decsriptions = session[round_number]
        return render_template('play.html', b_lines=b_lines, repo_1=repos[0][0], repo_2 =repos[1][0], repo_3 =repos[2][0], repo_4 =repos[3][0], index=index, repo_dsc=repo_decsriptions)   
    
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

    session[round_number] = [b_lines, repos, index, repo_decsriptions]

    return render_template('play.html', b_lines=b_lines, repo_1=repos[0][0], repo_2 =repos[1][0], repo_3 =repos[2][0], repo_4 =repos[3][0], index=index, repo_dsc=repo_decsriptions)   

@app.route('/result',methods = ['POST', 'GET'])
def result():
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