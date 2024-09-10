import React, { useState } from 'react';

function Chatbot() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:8000/ask/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: input }),
    });
    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-md w-96">
        <h1 className="text-xl font-bold mb-4">Recruiter Chatbot</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="border p-2 w-full mb-4"
            placeholder="Haz tu pregunta"
          />
          <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded">
            Preguntar
          </button>
        </form>
        {response && <p className="mt-4 text-gray-700">{response}</p>}
      </div>
    </div>
  );
}

export default Chatbot;
