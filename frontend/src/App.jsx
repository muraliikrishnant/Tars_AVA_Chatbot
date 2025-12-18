import React from 'react';
import ChatWidget from './components/ChatWidget';

function App() {
  return (
    <div className="App">
      <div style={{ padding: '40px', fontFamily: 'sans-serif', textAlign: 'center' }}>
        <h1>Tars Group Website (Mock)</h1>
        <p>Welcome to the Tars Group website. Explore our services.</p>
        <p>The chatbot "Ava" is located in the bottom right corner.</p>
      </div>
      <ChatWidget />
    </div>
  );
}

export default App;
