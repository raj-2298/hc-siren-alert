import socketio
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    allow_upgrades=False,
    transports=["polling"]
)

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve static HTML directly
@app.get("/")
async def get_home():
    return FileResponse("siren.html")

# Trigger siren
@app.post("/api/trigger")
async def trigger_alert():
    await sio.emit("mail_alert", {"message": "New Mail Received!"})
    return {"status": "siren played"}

# Combine apps
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
