from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

# Simple CORS without middleware
@app.middleware("http")
async def add_cors(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

process = None

@app.get("/logs")
def get_logs():
    global process
    if process:
        try:
            stdout, stderr = process.communicate(timeout=0.1)
            return {"stdout": stdout, "stderr": stderr, "returncode": process.returncode}
        except subprocess.TimeoutExpired:
            return {"status": "process running", "returncode": None}
        except:
            return {"error": "could not get logs"}
    return {"error": "no process"}

@app.get("/status")
def get_status():
    global process
    if process and process.poll() is None:
        return {"status": "started"}
    process = None
    return {"status": "not running"}

@app.post("/start")
def start_camera():
    global process
    if process and process.poll() is None:
        return {"status": "already running"}
    try:
        import sys
        print(f"Starting process with: {sys.executable}")
        print(f"Working directory: {os.path.dirname(__file__)}")
        process = subprocess.Popen(
            [sys.executable, "main.py"], 
            cwd=os.path.dirname(__file__),
            creationflags=subprocess.CREATE_NEW_CONSOLE  # Create new console window
        )
        return {"status": "started"}
    except Exception as e:
        print(f"Error starting process: {e}")
        return {"status": "not running"}

@app.post("/stop")
def stop_camera():
    global process
    if process:
        process.terminate()
        process = None
    return {"status": "stopped"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)