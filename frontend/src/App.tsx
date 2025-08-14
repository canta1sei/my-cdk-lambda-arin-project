import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// Note: The API Gateway URL will be the root path of the deployment.
// For local development, you might need to configure a proxy in vite.config.ts 
// to forward requests from http://localhost:5173/ to your actual API Gateway endpoint.
const API_ENDPOINT = "/api"; 

function App() {
  const [text, setText] = useState<string>('');
  const [responseText, setResponseText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResponseText('');

    try {
      // The backend expects the format: { "inputTranscript": "..." }
      const requestBody = {
        "inputTranscript": text
      };

      const result = await axios.post(API_ENDPOINT, requestBody);

      // The backend returns the format: { "response": "..." }
      setResponseText(result.data.response);
    } catch (err) {
      setError('An error occurred while fetching the response. Please try again.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Gemini Chat</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="text-input">Your Message:</label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type your message here..."
            required
          />
        </div>

        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Generating...' : 'Send'}
        </button>
      </form>

      {error && <div className="error-area"><p>{error}</p></div>}

      {responseText && (
        <div className="response-area">
          <h2>Response:</h2>
          <p>{responseText}</p>
        </div>
      )}
    </div>
  );
}

export default App;
