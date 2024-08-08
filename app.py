from flask import Flask, render_template
import time
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/room")
def room():
    chats = [
        {
            "user": "Rahat006",
            "message": "Fuck You!",
            "time": time.time()
        },
        {
            "user": "Rahat007",
            "message": "Fuck You more!",
            "time": time.time()
        },
    ]
    return render_template("room.html", chats=chats)


if (__name__ == "__main__"):
    app.run(debug=True)

