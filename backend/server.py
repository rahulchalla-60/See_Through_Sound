from fastapi import FastAPI
import subprocess
import signal
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import sys

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite (your React app)
        "http://localhost:3000",   # CRA (optional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

process = None

# Serve static HTML
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/status")
def get_status():
    global process
    if process is None:
        return {"status": "not running"}
    if process.poll() is not None:
        process = None  # Reset if process died
        return {"status": "not running"}
    return {"status": "started"}


@app.post("/start")
def start_backend():
    global process
    if process is not None and process.poll() is None:
        return {"status": "already running"}
    
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        return {"status": "started"}
    except Exception:
        process = None
        return {"status": "not running"}


@app.post("/stop")
def stop_backend():
    global process
    if process is None:
        return {"status": "not running"}
    
    try:
        if process.poll() is None:  # Process is still running
            process.send_signal(signal.CTRL_BREAK_EVENT)
        process = None
        return {"status": "stopped"}
    except Exception:
        process = None
        return {"status": "stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
