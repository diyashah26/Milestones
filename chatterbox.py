from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

# -----------------------------
# Data Structures
# -----------------------------
active_connections = []
usernames = {}
rooms = {}

# -----------------------------
# HTML Frontend
# -----------------------------
html = """
<!DOCTYPE html>
<html>
<head>
<title>Chatterbox Final</title>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body { 
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #f1f3f4 100%);
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    
    /* Header */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .header h1 {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .header p {
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Main Container */
    .main-container {
        flex: 1;
        display: flex;
        max-height: calc(100vh - 80px);
    }
    
    /* Sidebar */
    .sidebar {
        width: 280px;
        background: white;
        border-right: 1px solid #e1e5e9;
        display: flex;
        flex-direction: column;
        box-shadow: 2px 0 5px rgba(0,0,0,0.05);
    }
    
    .user-section {
        padding: 20px;
        border-bottom: 1px solid #e1e5e9;
        text-align: center;
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        margin: 0 auto 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 18px;
        font-weight: 600;
    }
    
    .user-name {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin-bottom: 5px;
    }
    
    .user-status {
        font-size: 12px;
        color: #28a745;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        background: #28a745;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .rooms-section {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
    }
    
    .rooms-title {
        font-size: 12px;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 15px;
    }
    
    .room-item {
        padding: 12px 15px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 14px;
        color: #495057;
        border: 1px solid transparent;
    }
    
    .room-item:hover {
        background: #f8f9fa;
        transform: translateX(3px);
    }
    
    .room-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .room-icon {
        font-size: 16px;
    }
    
    /* Chat Area */
    .chat-area {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: #ffffff;
    }
    
    .chat-header {
        padding: 15px 20px;
        background: #f8f9fa;
        border-bottom: 1px solid #e1e5e9;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .current-room {
        font-size: 18px;
        font-weight: 600;
        color: #333;
    }
    
    .room-info {
        font-size: 12px;
        color: #6c757d;
    }
    
    /* Messages */
    .messages {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #fafbfc;
    }
    
    .messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .messages::-webkit-scrollbar-track {
        background: #f1f3f4;
    }
    
    .messages::-webkit-scrollbar-thumb {
        background: #c1c8cd;
        border-radius: 3px;
    }
    
    .message {
        margin-bottom: 15px;
        display: flex;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .message.own {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 10px 15px;
        border-radius: 18px;
        position: relative;
    }
    
    .message.other .message-bubble {
        background: #e9ecef;
        color: #333;
        border: 1px solid #dee2e6;
    }
    
    .message.own .message-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    .message-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
        font-size: 11px;
        opacity: 0.7;
    }
    
    .message-author {
        font-weight: 600;
    }
    
    .message-time {
        opacity: 0.7;
    }
    
    .message-content {
        font-size: 14px;
        line-height: 1.4;
        word-wrap: break-word;
    }
    
    .message.system {
        justify-content: center;
    }
    
    .message.system .message-bubble {
        background: #e7f3ff;
        color: #0066cc;
        border: 1px solid #b3d9ff;
        text-align: center;
        font-style: italic;
        font-size: 13px;
        max-width: 80%;
    }
    
    /* Typing Indicator */
    .typing-indicator {
        padding: 10px 20px;
        font-size: 13px;
        color: #6c757d;
        font-style: italic;
        background: #f8f9fa;
        border-top: 1px solid #e1e5e9;
        min-height: 20px;
    }
    
    /* Input Area */
    .input-area {
        padding: 20px;
        background: white;
        border-top: 1px solid #e1e5e9;
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .input-wrapper {
        flex: 1;
        position: relative;
    }
    
    #msg {
        width: 100%;
        padding: 12px 15px;
        border: 2px solid #e1e5e9;
        border-radius: 25px;
        font-size: 14px;
        background: #f8f9fa;
        transition: all 0.3s ease;
        font-family: inherit;
    }
    
    #msg:focus {
        outline: none;
        border-color: #667eea;
        background: white;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    #msg::placeholder {
        color: #6c757d;
    }
    
    .send-button {
        padding: 12px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .send-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .send-button:active {
        transform: translateY(0);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .sidebar {
            width: 220px;
        }
        
        .message-bubble {
            max-width: 85%;
        }
    }
</style>
</head>
<body>

<div class="header">
    <h1>💬 Chatterbox</h1>
    <p>Real-Time Room-Based Chat</p>
</div>

<div class="main-container">
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="user-section">
            <div class="user-avatar" id="userAvatar">A</div>
            <div class="user-name" id="userName">Anonymous</div>
            <div class="user-status">
                <div class="status-dot"></div>
                <span>Online</span>
            </div>
        </div>
        
        <div class="rooms-section">
            <div class="rooms-title">Rooms</div>
            <div class="room-item active" data-room="general">
                <span class="room-icon">💬</span>
                <span>General</span>
            </div>
            <div class="room-item" data-room="tech">
                <span class="room-icon">💻</span>
                <span>Tech Talk</span>
            </div>
            <div class="room-item" data-room="fun">
                <span class="room-icon">🎮</span>
                <span>Fun Zone</span>
            </div>
        </div>
    </div>
    
    <!-- Chat Area -->
    <div class="chat-area">
        <div class="chat-header">
            <div>
                <div class="current-room" id="currentRoom">💬 General</div>
                <div class="room-info">Real-time messaging</div>
            </div>
        </div>
        
        <div class="messages" id="chat"></div>
        
        <div class="typing-indicator" id="typing"></div>
        
        <div class="input-area">
            <div class="input-wrapper">
                <input id="msg" placeholder="Type your message..." autocomplete="off">
            </div>
            <button class="send-button" onclick="sendMessage()">Send</button>
        </div>
    </div>
</div>

<script>

const chat = document.getElementById("chat");
const typingDiv = document.getElementById("typing");
const roomItems = document.querySelectorAll('.room-item');
const currentRoomEl = document.getElementById("currentRoom");
const userNameEl = document.getElementById("userName");
const userAvatarEl = document.getElementById("userAvatar");

let username = prompt("Enter your name:") || "Anonymous";
let currentRoom = "general";

// Update user info
userNameEl.textContent = username;
userAvatarEl.textContent = username.charAt(0).toUpperCase();

const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
    socket.send(JSON.stringify({
        type:"join",
        username:username,
        room:currentRoom
    }));
};

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if(data.type === "chat"){
        // Only add message if it's not from yourself
        if(data.username !== username){
            addMessage(data.username, data.message, false);
        }
    }
    
    if(data.type === "system"){
        addSystemMessage(data.message);
    }
    
    if(data.type === "typing"){
        typingDiv.innerText = data.username + " is typing...";
        return;
    }
    
    if(data.type === "stop_typing"){
        typingDiv.innerText = "";
        return;
    }
};

function addMessage(author, content, isOwn = false) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${isOwn ? 'own' : 'other'}`;
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            <div class="message-header">
                <span class="message-author">${author}</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-content">${content}</div>
        </div>
    `;
    
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
}

function addSystemMessage(content) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message system";
    
    messageDiv.innerHTML = `
        <div class="message-bubble">
            <div class="message-content">${content}</div>
        </div>
    `;
    
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight;
}

function sendMessage(){
    const msg = document.getElementById("msg").value;
    
    if(msg === "") return;
    
    // Add own message immediately
    addMessage(username, msg, true);
    
    socket.send(JSON.stringify({
        type:"chat",
        message:msg
    }));
    
    socket.send(JSON.stringify({
        type:"stop_typing"
    }));
    
    document.getElementById("msg").value = "";
}

// Room switching
roomItems.forEach(item => {
    item.addEventListener('click', () => {
        const newRoom = item.dataset.room;
        
        // Update active state
        roomItems.forEach(r => r.classList.remove('active'));
        item.classList.add('active');
        
        // Update current room display
        currentRoom = newRoom;
        currentRoomEl.innerHTML = item.innerHTML;
        
        // Clear chat
        chat.innerHTML = "";
        typingDiv.innerText = "";
        
        // Join new room
        socket.send(JSON.stringify({
            type:"join",
            username:username,
            room:newRoom
        }));
    });
});

// Typing indicator
let typingTimer;
document.getElementById("msg").addEventListener("input", ()=>{
    socket.send(JSON.stringify({type:"typing"}));
    
    clearTimeout(typingTimer);
    typingTimer = setTimeout(() => {
        socket.send(JSON.stringify({type:"stop_typing"}));
    }, 1000);
});

// Enter key support
document.getElementById("msg").addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

</script>

</body>
</html>
"""

# ----------------------------------------------------
# 2. Simple GET API to check the server
# ----------------------------------------------------
@app.get("/api")
async def read_root():
    return {"message": "Chatterbox Milestone 4 - Final Production Ready Chat Server", "active_connections": len(active_connections)}

# ----------------------------------------------------
# 3. Main HTML UI
# ----------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return html

# -----------------------------
# Broadcast function
# -----------------------------
async def broadcast(room,data):

    for connection in active_connections:
        if rooms.get(connection) == room:
            await connection.send_json(data)

# -----------------------------
# WebSocket Endpoint
# -----------------------------
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

            # Handle room changes
            if data["type"] == "join":
                old_room = rooms.get(ws, room)
                new_room = data.get("room", room)
                
                # Update user's room
                rooms[ws] = new_room
                
                # Broadcast leave message to old room
                if old_room != new_room:
                    await broadcast(old_room,{
                        "type":"system",
                        "message":f"{username} left {old_room} ❌"
                    })
                
                # Broadcast join message to new room
                await broadcast(new_room,{
                    "type":"system",
                    "message":f"{username} joined {new_room} 👋"
                })
                
                # Update current room for this user
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

# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    uvicorn.run("chatterbox:app",host="localhost",port=8000,reload=True)
