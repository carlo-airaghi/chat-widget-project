// widget/chat-widget.js

(function () {
  // Configuration
  const apiUrl = 'http://127.0.0.1:5000/chat'; // Update with your backend URL

  // Create the chat widget container
  const widgetContainer = document.createElement('div');
  widgetContainer.id = 'chat-widget-container';

  // Header
  const header = document.createElement('div');
  header.id = 'chat-widget-header';

  // Create the logo image element
  const logoImg = document.createElement('img');
  logoImg.id = 'chat-widget-logo';
  logoImg.src = 'BMW_logo.png'; // Ensure the path is correct
  logoImg.alt = 'BMW Logo';

  // Add the logo to the header
  header.appendChild(logoImg);

  // Add the header text
  const headerText = document.createElement('span');
  headerText.id = 'chat-widget-header-text';
  headerText.innerText = 'BMW Chat Assistant';

  // Add the header text to the header
  header.appendChild(headerText);

  // Add the header to the widget container
  widgetContainer.appendChild(header);

  // Chat history
  const chatHistory = document.createElement('div');
  chatHistory.id = 'chat-widget-history';
  widgetContainer.appendChild(chatHistory);

  // Input container
  const inputContainer = document.createElement('div');
  inputContainer.id = 'chat-widget-input-container';

  const inputField = document.createElement('input');
  inputField.type = 'text';
  inputField.placeholder = 'Type a message...';
  inputField.id = 'chat-widget-input';
  inputContainer.appendChild(inputField);

  const sendButton = document.createElement('button');
  sendButton.id = 'chat-widget-send-button';
  sendButton.innerText = 'Send';
  inputContainer.appendChild(sendButton);

  widgetContainer.appendChild(inputContainer);

  // Append the widget to the body
  document.body.appendChild(widgetContainer);

  // Include CSS file
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.type = 'text/css';
  link.href = 'chat-widget.css'; // Ensure the path is correct
  document.head.appendChild(link);

  // Function to display messages
  function displayMessage(sender, message) {
    const messageContainer = document.createElement('div');
    messageContainer.classList.add('chat-widget-message');
    messageContainer.classList.add(
      sender === 'user' ? 'chat-widget-message-user' : 'chat-widget-message-bot'
    );

    const messageBubble = document.createElement('div');
    messageBubble.classList.add('chat-widget-bubble');
    messageBubble.innerText = message;

    messageContainer.appendChild(messageBubble);
    chatHistory.appendChild(messageContainer);

    // Allow time for rendering
    setTimeout(() => {
      const messageTop = messageContainer.offsetTop;
      const messageHeight = messageContainer.offsetHeight;
      const containerHeight = chatHistory.clientHeight;

      // Calculate the scroll position to center the new message
      const scrollPosition = messageTop - (containerHeight / 3);

      // Scroll to the calculated position
      chatHistory.scrollTo({
        top: scrollPosition,
        behavior: 'smooth',
      });
    }, 0);
  }



  // Function to send message
  function sendMessage() {
    const message = inputField.value.trim();
    if (message === '') return;

    displayMessage('user', message);
    inputField.value = '';

    // Send the message to the backend server
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.reply) {
          displayMessage('bot', data.reply);
        } else {
          displayMessage('bot', 'Sorry, something went wrong.');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        displayMessage('bot', 'Sorry, there was an error. Please try again later.');
      });
  }

  // Event listeners
  sendButton.addEventListener('click', sendMessage);
  inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      sendMessage();
    }
  });
})();
