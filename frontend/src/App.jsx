import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState('not running');
  const [loading, setLoading] = useState(false);

  const isRunning = status === 'started' || status === 'already running';
  const isStopped = status === 'stopped' || status === 'not running' || status === 'backend unreachable';

  // Fetch initial status on component mount
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch('http://127.0.0.1:8000/status');
        const data = await res.json();
        setStatus(data.status);
      } catch {
        setStatus('backend unreachable');
      }
    };
    fetchStatus();
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key.toLowerCase() === 's' && !isRunning && !loading) {
        handleStart();
      } else if (event.key.toLowerCase() === 'x' && !isStopped && !loading) {
        handleStop();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }); // Remove dependencies array to avoid stale closure issue

  const handleStart = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      setStatus(data.status);
    } catch (error) {
      console.error('Error starting backend:', error);
      setStatus('backend unreachable');
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    // Confirmation dialog
    if (!window.confirm("Stop camera?")) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/stop', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      const data = await response.json();
      setStatus(data.status);
    } catch (error) {
      console.error('Error stopping backend:', error);
      setStatus('backend unreachable');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">See Through Sound</h1>
      <h2 className="subtitle">Camera Control Panel</h2>
      
      <div className="button-container">
        <button
          onClick={handleStart}
          disabled={isRunning || loading}
          className={`button start-button ${(isRunning || loading) ? 'disabled-button' : ''}`}
        >
          {loading && !isRunning ? 'Starting...' : 'Start Camera'}
        </button>
        
        <button
          onClick={handleStop}
          disabled={isStopped || loading}
          className={`button stop-button ${(isStopped || loading) ? 'disabled-button' : ''}`}
        >
          {loading && isRunning ? 'Stopping...' : 'Stop Camera'}
        </button>
      </div>
      
      <div className="status-container">
        <p className="status-label">Status:</p>
        <p className={`status-text ${
          isRunning ? 'status-running' : 
          isStopped ? 'status-stopped' : 
          'status-error'
        }`}>
          {status}
        </p>
      </div>
      
      <div className="help-text">
        <p>Keyboard shortcuts: <strong>S</strong> = Start, <strong>X</strong> = Stop</p>
      </div>
    </div>
  );
}

export default App
