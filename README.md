# 💬 Chatterbox – Real-Time Room-Based Chat Application

Chatterbox is a real-time chat application built using FastAPI and WebSockets.  
It allows multiple users to connect simultaneously and communicate inside separate chat rooms.

This project demonstrates real-time communication using WebSocket connections and includes features like room-based messaging and typing indicators.

--------------------------------------------------

🚀 Features

• Real-time messaging using WebSockets  
• Multiple chat rooms (General, Tech, Fun)  
• Typing indicator when a user is typing  
• Room switching support  
• Join and leave notifications  
• Simple and clean HTML + CSS interface  
• Lightweight backend using FastAPI  

--------------------------------------------------

🛠️ Technologies Used

• Python  
• FastAPI  
• WebSockets  
• Uvicorn  
• HTML  
• CSS  
• JavaScript  

--------------------------------------------------

📂 Project Structure

chatterbox/
│
├── chatterbox.py        # Main FastAPI chat server
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies

--------------------------------------------------

⚙️ Installation

1. Clone the repository

git clone https://github.com/diyashah26/chatterbox.git
cd chatterbox

2. Install dependencies

pip install -r requirements.txt

--------------------------------------------------

▶️ Run the Server

Start the application using:

python chatterbox.py

The server will start at:

http://localhost:8000

--------------------------------------------------

🌐 How to Use

1. Open your browser and go to:

http://localhost:8000

2. Enter your username when prompted.

3. Select a chat room:
   • General
   • Tech
   • Fun

4. Start chatting with other connected users.

5. Open multiple browser tabs or different browsers to simulate multiple users.

--------------------------------------------------

🔄 How It Works

1. A user connects to the server using WebSockets.
2. The user joins a chat room.
3. Messages are broadcast only to users in the same room.
4. The server manages active connections, usernames, and room assignments.

Events handled by the server:
• User joining a room
• Sending messages
• Typing indicators
• Stopping typing indicator
• User disconnecting

--------------------------------------------------

📡 API Endpoint

A simple API endpoint is available to check if the server is running.

GET /api

Example response:

{
  "message": "Chatterbox Milestone 4 - Final Production Ready Chat Server",
  "active_connections": 2
}

--------------------------------------------------

🧪 Testing

To test multiple users:

• Open multiple browser tabs  
• Or open different browsers  
• Join the same or different rooms to test room-based messaging  

--------------------------------------------------

👩‍💻 Author

Diya Shah