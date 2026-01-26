# See Through Sound - Frontend

React frontend controller for the computer vision backend.

## Setup & Run

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the React app:**
   ```bash
   npm start
   ```
   - Opens at http://localhost:3000
   - Make sure backend is running at http://127.0.0.1:8000

3. **Usage:**
   - Click "Start Camera" to begin object detection
   - Click "Stop Camera" to end detection
   - Status updates automatically
   - Buttons are disabled based on current state

## Architecture

```
React Frontend (localhost:3000)
    ↓ HTTP POST
FastAPI Backend (127.0.0.1:8000)
    ↓ subprocess
Python main.py (camera + detection)
```

## Features

- ✅ Smart button states (disabled when appropriate)
- ✅ Loading indicators
- ✅ Error handling
- ✅ Clean, responsive UI
- ✅ No external dependencies
- ✅ Production-ready code