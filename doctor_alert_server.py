import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    allow_upgrades=False,
    transports=['polling']
)

fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")

@fastapi_app.get("/")
async def root():
    return {"message": "Siren server is running"}

@fastapi_app.post("/api/trigger")
async def trigger_alert():
    await sio.emit("mail_alert", {"message": "New Mail Received!"})
    return {"status": "alert emitted"}

app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
