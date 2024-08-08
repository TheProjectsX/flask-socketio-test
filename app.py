from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
import time
from string import ascii_letters
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "NeverGonnaGiveYouUp1773"
socketio = SocketIO(app)
rooms = {}


def getNewRoomCode(length=5):
    code = "".join([random.choice(ascii_letters) for x in range(length)])
    if (code in rooms):
        code = getNewRoomCode(length)
    
    return code

@app.route("/", methods=["GET", "POST"])
def home():
    if (request.method == "GET"):
        return render_template("index.html")
    
    name = request.form.get("name", "")
    roomId = request.form.get("roomId", "")

    if (name == ""):
        return render_template("index.html", error="Please add a Name first", roomId=roomId)
    
    if (roomId == ""):
        roomId = getNewRoomCode()
        rooms[roomId] = {"members": 0, "messages": []}
    elif (roomId not in rooms):
        return render_template("index.html", error="No Room Found!", name=name, roomId=roomId)
    
    session["name"] = name
    session["roomId"] = roomId

    return redirect("/room")

@app.route("/room")
def room():
    name = session.get("name")
    roomId = session.get("roomId")

    if (name is None or roomId is None):
        return redirect("/")

    return render_template("room.html", roomId=roomId)


if (__name__ == "__main__"):
    socketio.run(app, debug=True)

