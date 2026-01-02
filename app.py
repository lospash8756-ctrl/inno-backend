import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';

const VoiceChat = () => {
  const [username, setUsername] = useState('');
  const [status, setStatus] = useState('Warte auf Eingabe...');
  const [logs, setLogs] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  
  // HIER DEINE PYTHON-BACKEND URL EINFÜGEN (Wenn du es deployt hast)
  // Wenn du lokal testest: "http://localhost:5000"
  const BACKEND_URL = "HIER_DEINE_RENDER_URL_EINFÜGEN"; 

  const socketRef = useRef(null);

  const addLog = (msg) => {
    setLogs(prev => [...prev, msg]);
    console.log(msg);
  };

  const connectVoice = () => {
    if (!username) {
      alert("Bitte Namen eingeben!");
      return;
    }

    setStatus("Versuche Verbindung...");
    addLog(`Verbinde zu Backend: ${BACKEND_URL}`);

    // Verbindung zum Python Backend (nicht direkt zu Aternos, das geht im Browser nicht)
    socketRef.current = io(BACKEND_URL);

    socketRef.current.on('connect', () => {
      setStatus("Verbunden mit Backend!");
      setIsConnected(true);
      addLog("WebSocket Verbindung steht.");
      
      // Sende den Namen an das Backend
      socketRef.current.emit('join_request', { username: username });
    });

    socketRef.current.on('connect_error', (err) => {
      setStatus("Verbindungsfehler!");
      addLog("Fehler: " + err.message);
    });

    socketRef.current.on('disconnect', () => {
      setStatus("Getrennt.");
      setIsConnected(false);
      addLog("Verbindung unterbrochen.");
    });
    
    // Hier würdest du Antworten vom Server empfangen
    socketRef.current.on('voice_data', (data) => {
        // Audio verarbeiten...
    });
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h2>🔊 Simple Voice Chat (React)</h2>
        <p>Aternos Bridge</p>

        <input
          style={styles.input}
          type="text"
          placeholder="Dein Minecraft Name"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          disabled={isConnected}
        />
        <br />
        <button 
          style={styles.button} 
          onClick={connectVoice}
          disabled={isConnected}
        >
          {isConnected ? "Verbunden" : "Verbinden"}
        </button>

        <div style={{...styles.status, color: isConnected ? 'green' : '#ffcc00'}}>
          {status}
        </div>
      </div>

      <div style={styles.logBox}>
        <h3>Logs:</h3>
        {logs.map((log, index) => (
          <div key={index} style={styles.logItem}>&gt; {log}</div>
        ))}
      </div>
    </div>
  );
};

// Einfaches Styling für React
const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    color: 'white',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '20px',
    fontFamily: 'Arial, sans-serif'
  },
  box: {
    backgroundColor: '#333',
    padding: '20px',
    borderRadius: '10px',
    width: '100%',
    maxWidth: '400px',
    textAlign: 'center',
    marginBottom: '20px'
  },
  input: {
    padding: '10px',
    width: '80%',
    margin: '10px 0',
    borderRadius: '5px',
    border: 'none'
  },
  button: {
    padding: '10px 20px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    fontSize: '16px'
  },
  status: {
    marginTop: '20px',
    fontWeight: 'bold'
  },
  logBox: {
    width: '100%',
    maxWidth: '600px',
    textAlign: 'left',
    fontSize: '12px',
    color: '#aaa',
    borderTop: '1px solid #444',
    paddingTop: '10px'
  },
  logItem: {
    marginBottom: '2px'
  }
};

export default VoiceChat;
