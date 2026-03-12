from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

active_connections = []
usernames = {}
rooms = {}

html = """
<!DOCTYPE html>
<html>
<head>
<title>Chatterbox - Real-Time Chat</title>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body { 
        font-family: Arial, sans-serif;
        background: #f5f5f5;
        padding: 20px;
    }
    
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        background: white;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header {
        background: #2563eb;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 8px 8px 0 0;
    }
    
    .header h1 {
        font-size: 24px;
        margin-bottom: 5px;
    }
    
    .header p {
        font-size: 14px;
        opacity: 0.9;
    }
    
    .controls {
        padding: 20px;
        border-bottom: 1px solid #eee;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .controls label {
        font-weight: bold;
        color: #333;
    }
    
    #room {
        padding: 8px 12px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
        background: white;
    }
    
    #room:focus {
        outline: none;
        border-color: #2563eb;
    }
    
    #chat {
        height: 400px;
        overflow-y: auto;
        padding: 20px;
        background: #fafafa;
    }
    
    #chat::-webkit-scrollbar {
        width: 6px;
    }
    
    #chat::-webkit-scrollbar-thumb {
        background: #ccc;
        border-radius: 3px;
    }
    
    .message {
        margin-bottom: 12px;
        padding: 10px 14px;
        border-radius: 8px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .message.system {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        text-align: center;
        font-style: italic;
        color: #856404;
        margin: 10px auto;
        font-size: 13px;
    }
    
    .message.chat {
        background: white;
        border: 1px solid #e9ecef;
        color: #333;
    }
    
    .message.chat strong {
        color: #2563eb;
        font-weight: bold;
        display: block;
        margin-bottom: 4px;
        font-size: 12px;
    }
    
    #typing {
        padding: 10px 20px;
        color: #28a745;
        font-size: 13px;
        font-style: italic;
        background: #f8f9fa;
        border-top: 1px solid #eee;
        min-height: 20px;
    }
    
    .input-area {
        padding: 20px;
        background: white;
        border-top: 1px solid #eee;
        display: flex;
        gap: 10px;
    }
    
    #msg {
        flex: 1;
        padding: 10px 14px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 14px;
    }
    
    #msg:focus {
        outline: none;
        border-color: #2563eb;
    }
    
    button {
        padding: 10px 20px;
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }
    
    button:hover {
        background: #1d4ed8;
    }
</style>
</head>
<body>

<div class="chat-container">
    <div class="header">
        <h1>💬 Chatterbox</h1>
        <p>Real-Time Room-Based Chat Application</p>
    </div>
    
    <div class="controls">
        <label for="room">Room:</label>
        <select id="room">
            <option value="general">💬 General</option>
            <option value="tech">💻 Tech</option>
            <option value="fun">🎮 Fun</option>
        </select>
    </div>
    
    <div id="chat"></div>
    <div id="typing"></div>
    
    <div class="input-area">
        <input id="msg" placeholder="Type your message..." autocomplete="off">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>

const chat = document.getElementById("chat");
const typingDiv = document.getElementById("typing");
const roomSelect = document.getElementById("room");

let username = prompt("Enter your name:") || "Anonymous";

const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {

    socket.send(JSON.stringify({
        type:"join",
        username:username,
        room:roomSelect.value
    }));

};

socket.onmessage = (event) => {

    const data = JSON.parse(event.data);
    const div = document.createElement("div");

    if(data.type === "chat"){
        div.className = "message chat";
        div.innerHTML = "<strong>"+data.username+":</strong> " + data.message;
    }

    if(data.type === "system"){
        div.className = "message system";
        div.innerText = data.message;
    }

    if(data.type === "typing"){
        typingDiv.innerText = data.username + " is typing...";
        return;
    }

    if(data.type === "stop_typing"){
        typingDiv.innerText = "";
        return;
    }

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;

};

function sendMessage(){

    const msg = document.getElementById("msg").value;

    if(msg === "") return;

    socket.send(JSON.stringify({
        type:"chat",
        message:msg
    }));

    socket.send(JSON.stringify({
        type:"stop_typing"
    }));

    document.getElementById("msg").value = "";
}

document.getElementById("msg").addEventListener("input", ()=>{
    socket.send(JSON.stringify({type:"typing"}));
});

// Add room change functionality
roomSelect.addEventListener("change", ()=>{
    const newRoom = roomSelect.value;
    
    // Clear chat when switching rooms
    chat.innerHTML = "";
    typingDiv.innerText = "";
    
    socket.send(JSON.stringify({
        type:"join",
        username:username,
        room:newRoom
    }));
});

// Add enter key support
document.getElementById("msg").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

</script>

</body>
</html>
"""

@app.get("/api")
async def read_root():
    return {"message": "Chatterbox Milestone 4 - Final Production Ready Chat Server", "active_connections": len(active_connections)}

@app.get("/", response_class=HTMLResponse)
async def home():
    return html

async def broadcast(room,data):

    for connection in active_connections:
        if rooms.get(connection) == room:
            await connection.send_json(data)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):

    await ws.accept()

    try:
        data = await ws.receive_json()

        username = data.get("username","Anonymous")
        room = data.get("room","general")

        active_connections.append(ws)
        usernames[ws] = username
        rooms[ws] = room

        await broadcast(room,{
            "type":"system",
            "message":f"{username} joined {room} 👋"
        })

        while True:

            data = await ws.receive_json()

            if data["type"] == "join":
                old_room = rooms.get(ws, room)
                new_room = data.get("room", room)
            
                rooms[ws] = new_room
                
                if old_room != new_room:
                    await broadcast(old_room,{
                        "type":"system",
                        "message":f"{username} left {old_room} ❌"
                    })
                
                await broadcast(new_room,{
                    "type":"system",
                    "message":f"{username} joined {new_room} 👋"
                })
                
                room = new_room

            elif data["type"] == "chat":

                await broadcast(room,{
                    "type":"chat",
                    "username":username,
                    "message":data["message"]
                })

            elif data["type"] == "typing":

                await broadcast(room,{
                    "type":"typing",
                    "username":username
                })

            elif data["type"] == "stop_typing":

                await broadcast(room,{
                    "type":"stop_typing"
                })

    except WebSocketDisconnect:

        left_user = usernames.get(ws,"Someone")
        room = rooms.get(ws)

        if ws in active_connections:
            active_connections.remove(ws)

        usernames.pop(ws,None)
        rooms.pop(ws,None)

        await broadcast(room,{
            "type":"system",
            "message":f"{left_user} left {room} ❌"
        })

if __name__ == "__main__":
    uvicorn.run("chatterbox:app",host="localhost",port=8000,reload=True)
