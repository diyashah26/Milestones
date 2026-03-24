# 💬 Chatterbox - Real-Time Chat Application

A modern, real-time chat application built with FastAPI and WebSocket, featuring room-based messaging, typing indicators, and a beautiful UI.

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies
```bash
pip install fastapi uvicorn websockets
```

### Run the Application
```bash
python chatterbox.py
```

The server will start at `http://localhost:8000`

## 📖 Usage

1. **Open your browser** and navigate to `http://localhost:8000`
2. **Enter your username** when prompted
3. **Select a room** from the sidebar (General, Tech Talk, or Fun Zone)
4. **Start chatting!** Type your message and press Enter or click Send

### Room Navigation
- Click on any room in the sidebar to switch
- Messages are isolated per room
- Chat history clears when switching rooms
- System notifications show join/leave events

### Chat Features
- **Send messages**: Type and press Enter or click Send
- **See typing indicators**: When others are typing
- **View timestamps**: All messages show time
- **Own messages**: Appear on the right with gradient styling
- **Other messages**: Appear on the left with light background
