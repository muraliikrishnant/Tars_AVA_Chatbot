import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';
import './ChatWidget.css';

// Get API URL from environment or default to production
const API_URL = import.meta.env.VITE_API_URL || process.env.REACT_APP_API_URL || 'https://tars-ava-chatbot.onrender.com';

const ChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { role: 'model', content: 'Hi, this is Ava. How may I help you today?' }
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputValue.trim()) return;

        const userMessage = { role: 'user', content: inputValue };
        setMessages((prev) => [...prev, userMessage]);
        setInputValue('');
        setIsLoading(true);

        try {
            // Prepare history for the backend (excluding the very first greeting if needed, 
            // but backend handles history. We'll send the full visible history or just the new message 
            // depending on backend logic. The backend expects 'history' list.)

            // We'll send the last few messages as history to keep context
            const historyToSend = messages.map(m => ({ role: m.role, content: m.content }));

            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage.content,
                    history: historyToSend
                }),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            const botMessage = { role: 'model', content: data.response };
            setMessages((prev) => [...prev, botMessage]);

            if (data.action === 'contact_support') {
                setMessages((prev) => [
                    ...prev,
                    {
                        role: 'model',
                        content: 'Click here to visit our Contact Page.',
                        isLink: true,
                        linkUrl: 'https://tarsgroup.co/contact'
                    }
                ]);
            }

        } catch (error) {
            console.error('Error:', error);
            setMessages((prev) => [
                ...prev,
                { role: 'model', content: 'Sorry, I am having trouble connecting to the server right now.' }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-widget-container">
            {isOpen && (
                <div className="chat-window">
                    <div className="chat-header">
                        <div className="chat-header-title">
                            <div className="avatar">A</div>
                            <span>Ava Support</span>
                        </div>
                        <button onClick={toggleChat} className="close-button">
                            <X size={20} />
                        </button>
                    </div>

                    <div className="chat-messages">
                        {messages.map((msg, index) => (
                            <div key={index} className={`message ${msg.role}`}>
                                <div className="message-content">
                                    {msg.isLink ? (
                                        <a href={msg.linkUrl} target="_blank" rel="noopener noreferrer" className="contact-link">
                                            {msg.content}
                                        </a>
                                    ) : (
                                        msg.content
                                    )}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="message model">
                                <div className="message-content typing-indicator">
                                    <span>.</span><span>.</span><span>.</span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <form onSubmit={handleSendMessage} className="chat-input-form">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Type a message..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading || !inputValue.trim()}>
                            <Send size={18} />
                        </button>
                    </form>
                </div>
            )}

            <button className="chat-toggle-button" onClick={toggleChat}>
                {isOpen ? <X size={24} /> : <MessageCircle size={24} />}
            </button>
        </div>
    );
};

export default ChatWidget;
