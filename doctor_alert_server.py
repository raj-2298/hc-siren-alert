import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Create a Socket.IO Async Server with polling only
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True,
    allow_upgrades=False,
    transports=['polling']
)

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check
@app.get("/")
async def root():
    return {"message": "HC Siren Alert Server is running (Polling Mode)."}

# Webhook to emit mail alert
@app.post("/api/trigger")
async def trigger_alert():
    await sio.emit("mail_alert", {"message": "New Mail Received!"})
    return {"status": "siren played"}

# Create full ASGI app combining Socket.IO and FastAPI
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
