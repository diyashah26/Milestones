from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

connections = {}
usernames = {}

html = """
<!DOCTYPE html>
<html>
<head>
<title>Chatterbox</title>

<style>
body{
font-family: Arial;
margin:40px;
}

#chat{
border:1px solid gray;
height:300px;
overflow:auto;
padding:10px;
}

input{
padding:8px;
}

button{
padding:8px;
}
</style>

</head>

<body>

<h2>Chatterbox - WebSocket Chat</h2>

<div id="chat"></div>

<br>

<input id="msg" placeholder="Type message">
<button onclick="send()">Send</button>

<script>

const chat = document.getElementById("chat")

const username = prompt("Enter your name")

const ws = new WebSocket("ws://localhost:8000/ws")

ws.onopen = () => {
ws.send(JSON.stringify({username: username}))
}

ws.onmessage = (event) => {

const data = JSON.parse(event.data)

const div = document.createElement("div")

if(data.type === "chat"){
div.innerHTML = "<b>" + data.user + ":</b> " + data.message
}
else{
div.innerHTML = "<i>" + data.message + "</i>"
}

chat.appendChild(div)
chat.scrollTop = chat.scrollHeight

}

function send(){

const msg = document.getElementById("msg").value

if(msg === "") return

ws.send(JSON.stringify({message: msg}))

document.getElementById("msg").value = ""

}

</script>

</body>
</html>
"""

@app.get("/")
async def home():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_chat(ws: WebSocket):

    await ws.accept()

    try:
        data = await ws.receive_json()
        username = data.get("username", "Anonymous")

        connections[ws] = ws
        usernames[ws] = username

        await broadcast({
            "type": "system",
            "message": f"{username} joined the chat"
        })

        while True:

            data = await ws.receive_json()
            message = data.get("message")

            if message:

                # Milestone 1 smart responses
                if message.lower() == "hello":
                    message = "Server: Hello!"
                elif message.lower() == "bye":
                    message = "Server: Goodbye!"

                await broadcast({
                    "type": "chat",
                    "user": username,
                    "message": message
                })

    except WebSocketDisconnect:

        connections.pop(ws)
        left = usernames.pop(ws)

        await broadcast({
            "type": "system",
            "message": f"{left} left the chat"
        })

async def broadcast(data):

    for connection in connections:
        await connection.send_json(data)

if __name__ == "__main__":
    uvicorn.run("chatterbox:app", host="localhost", port=8000, reload=True)