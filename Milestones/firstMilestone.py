from fastapi import FastAPI,WebSocket
import uvicorn
app = FastAPI()
@app.get("/")
async def home():
    return {"message": "Milestone 1 - Smart WebSocket Server Running"}
@app.websocket("/ws")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    print("Client connected")

    await websocket.send_text("Server: Welcome to Chatterbox!")

    while True:
        try:
            msg = await websocket.receive_text()
            print("Received:", msg)
            if msg.lower() == "hello":
                reply = "Server:Hello"
            elif msg.lower() == "bye":
                reply = "Server:Goodbye"
            else:
                reply = f"Server: Message received -> {msg}"

            await websocket.send_text(reply)
        except Exception:
            print("Client disconnected")
            break

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
