from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send, join_room, leave_room
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
        rooms[roomId] = {"members": [], "messages": []}
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
    
    chats = rooms[roomId]["messages"]

    return render_template("room.html", roomId=roomId, chats=chats)


@socketio.on("connect")
def connect(auth):
    name = session.get("name")
    roomId = session.get("roomId")

    message = {
        "user": name,
        "message": "joined the room",
        "time": time.time(),
        "msgStyle": "font-style: italic"
    }

    if (name not in rooms[roomId]["members"]):
        rooms[roomId]["members"].append(name)

    join_room(roomId)    
    send(message, to=roomId)

@socketio.on("disconnect")
def disconnect():
    name = session.get("name")
    roomId = session.get("roomId")

    message = {
        "user": name,
        "message": "left the room",
        "time": time.time(),
        "msgStyle": "font-style: italic"
    }

    rooms[roomId]["members"].remove(name)
    if (len(rooms[roomId]["members"]) == 0):
        del rooms[roomId]

    leave_room(roomId)
    send(message, to=roomId)

@socketio.on("message")
def message(data):
    name = session.get("name")
    roomId = session.get("roomId")

    message = {
        "user": name,
        "message": data["message"],
        "time": time.time()
    }
    
    rooms[roomId]["messages"].append(message)
    send(message, to=roomId)

if (__name__ == "__main__"):
    socketio.run(app, debug=True)

