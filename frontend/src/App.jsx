import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState('not running')
  const [loading, setLoading] = useState(false)

  const fetchStatus = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8001/status')
      const data = await res.json()
      setStatus(data.status)
    } catch {
      setStatus('backend unreachable')
    }
  }

  const handleStart = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8001/start', { method: 'POST' })
      const data = await res.json()
      setStatus(data.status)
    } catch {
      setStatus('backend unreachable')
    }
    setLoading(false)
  }

  const handleStop = async () => {
    if (!confirm("Stop camera?")) return
    setLoading(true)
    try {
      const res = await fetch('http://127.0.0.1:8001/stop', { method: 'POST' })
      const data = await res.json()
      setStatus(data.status)
    } catch {
      setStatus('backend unreachable')
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchStatus()
    const handleKey = (e) => {
      if (e.key === 's' && status !== 'started' && !loading) handleStart()
      if (e.key === 'x' && status === 'started' && !loading) handleStop()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  })

  const isRunning = status === 'started' || status === 'already running'

  return (
    <div className="container">
      <h1 className="title">See Through Sound</h1>
      <h2 className="subtitle">Camera Control Panel</h2>
      
      <div className="button-container">
        <button 
          onClick={handleStart} 
          disabled={isRunning || loading}
          className={`button start-button ${isRunning || loading ? 'disabled-button' : ''}`}
        >
          {loading && !isRunning ? 'Starting...' : 'Start Camera'}
        </button>
        
        <button 
          onClick={handleStop} 
          disabled={!isRunning || loading}
          className={`button stop-button ${!isRunning || loading ? 'disabled-button' : ''}`}
        >
          {loading && isRunning ? 'Stopping...' : 'Stop Camera'}
        </button>
      </div>
      
      <div className="status-container">
        <p className="status-label">Status:</p>
        <p className={`status-text ${isRunning ? 'status-running' : 'status-stopped'}`}>
          {status}
        </p>
      </div>
      
      <div className="help-text">
        <p>Keyboard: <strong>S</strong> = Start, <strong>X</strong> = Stop</p>
      </div>
    </div>
  )
}

export default App