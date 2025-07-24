
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Create a Socket.IO Async Server with polling only (no WebSockets)
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True,
    allow_upgrades=False,        # Prevent WebSocket upgrade
    transports=['polling']       # Force use of long polling
)

# Create FastAPI app and attach socket.io server
app = FastAPI()
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, or replace with specific domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach the Socket.IO ASGI App
app.mount("/", socketio.ASGIApp(sio, app))

# Serve static files (if needed for frontend alerts)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint to check deployment
@app.get("/")
async def root():
    return {"message": "HC Siren Alert Server is running (Polling Mode)."}

# Emit alert from webhook (POST)
@app.post("/api/trigger")
async def trigger_alert():
    await sio.emit("mail_alert", {"message": "New Mail Received!"})
    return {"status": "siren played"}
