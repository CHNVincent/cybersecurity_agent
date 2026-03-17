/**
 * Frontend JavaScript for Cybersecurity Agent Interface
 * Connects the UI elements to the backend API
 */

document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.querySelector('.message-input');
    const sendIcon = document.querySelector('.send-icon');
    const attachIcon = document.querySelector('.attach-icon');
    
    // Auto-focus input
    messageInput.focus();
    
    // Auto-scroll to bottom
    scrollToBottom();
    
    // Prevent default form submission and handle Enter key
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send button click handler
    sendIcon.addEventListener('click', sendMessage);
    
    // Function to send message to backend
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add message to UI immediately
        addMessageToUI(message, 'user');
        messageInput.value = '';
        
        // Make API call to backend to process the message
        processUserMessage(message);
    }
    
    // Function to add message to UI
    function addMessageToUI(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(sender === 'user' ? 'user-message' : 'assistant-message');
        
        // Add the message content
        messageDiv.textContent = message;
        
        // Append to chat container
        chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Function to process user message via backend
    function processUserMessage(message) {
        fetch('/api/agent/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),  // Django CSRF protection
            },
            body: JSON.stringify({
                message: message,
                conversation_id: getCurrentConversationId(),
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received response:', data);
            
            if (data.response) {
                // Add bot response to UI
                addMessageToUI(data.response, 'assistant');
            } else if (data.error) {
                // Handle error
                addMessageToUI('Error: ' + data.error, 'assistant');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToUI('An error occurred while processing your request.', 'assistant');
        });
    }
    
    // Auto-scroll to the bottom of the chat
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Get current conversation ID (in a real implementation, this would be managed)
    function getCurrentConversationId() {
        // This would retrieve the active conversation ID
        // For now, we'll use a placeholder
        return sessionStorage.getItem('current_conv_id') || 'default';
    }
    
    // Get CSRF token for Django forms
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value || 
               getCookie('csrftoken');
    }
    
    // Helper function to get cookie value
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Add file attachment handling
    attachIcon.addEventListener('click', function() {
        alert('File attachment functionality would be implemented here');
        // In a real implementation, this would open a file picker
    });
    
    // Mock assistant response functionality for development
    // Remove this in production when backend is connected
    window.triggerMockResponse = function() {
        const responses = [
            "I've analyzed your query. Based on the information provided, I recommend the following security measures...",
            "Based on the security scan, I've found potential issues in your code that need attention:",
            "The code you submitted has been reviewed. The primary concerns are related to input sanitization.",
            "After reviewing your security implementation, I can see opportunities for improvement in the following areas:"
        ];
        const randomResponse = responses[Math.floor(Math.random() * responses.length)];
        setTimeout(() => addMessageToUI(randomResponse, 'assistant'), 1000);
    };
});