from flask import Flask, template

app = Flask(__name__)

app.route("/", stict_slashes=False)
def init():
    return template("0-index.html")

if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True)
