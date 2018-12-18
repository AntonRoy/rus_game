import os
import random
import pymongo
from flask import *

app = Flask(__name__)
db = pymongo.MongoClient('mongodb://localhost:27017/')["rus_game"]
app.static_folder = ""


@app.route("/", methods=['POST', 'GET'])
def start():
    if session['logged_in']:
        return redirect("/main")
    return redirect("/login")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = hash(request.form['password'])
        users = db['user'].find({"login" : login})
        if users.count():
            user = users.first()
            if hash(user.password) == password:
                session["logged_in"] = True
                return redirect("/main")
            else:
                return render_template("login.html", error="Неверный пароль :(")
        else:
            return render_template("login.html", error="Неверный логин :(")
    return render_template("login.html", error="")

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session['logged_in'] = False
    return redirect('/login')

@app.route("/main", methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        #работа со словами
        data = []
        return render_template("main.html", data=data)
    return render_template("main.html")

if __name__ == '__main__':
    print("started")
    app.run(host="0.0.0.0", port=8080)
