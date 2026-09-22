from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def indentifier():
    return render_template("indentifier.html")

@app.route("/profile")
def profile():
    mhobbies = ["야구", "여행", "Formula 1"]
    return render_template("profile.html", hobbies = mhobbies)

@app.route("/greet/<name>")
def greet(name):
    return render_template("greet.html", user = name)

if __name__ == "__main__":
    app.run(debug = True)