// widget/chat-widget.js

(function () {
  // Configuration
  const apiUrl = 'http://127.0.0.1:5000/chat'; // Update with your backend URL

  // Flags to track the chat and privacy state
  let isChatOpen = false;
  let isPrivacyAccepted = false;

  // Create the minimized chat icon
  const chatIcon = document.createElement('div');
  chatIcon.id = 'chat-widget-icon';
  chatIcon.title = 'Open Chat';

  // Create an image element for the chat icon
  const chatIconImg = document.createElement('img');
  chatIconImg.id = 'chat-widget-icon-img';
  chatIconImg.src = 'BMW_chat_icon.png'; // Ensure the path is correct
  chatIconImg.alt = 'Open Chat';
  chatIcon.appendChild(chatIconImg);

  // Append the icon to the body
  document.body.appendChild(chatIcon);

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

  // Add the header text
  const headerText = document.createElement('span');
  headerText.id = 'chat-widget-header-text';
  headerText.innerText = 'Virtual Assistant';

  // Add the minimize button
  const minimizeButton = document.createElement('img');
  minimizeButton.id = 'chat-widget-minimize-button';
  minimizeButton.src = 'BMW_arrow_down.png'; // Ensure the path is correct
  minimizeButton.alt = 'Minimize Chat';

  // Add the close button
  const closeButton = document.createElement('img');
  closeButton.id = 'chat-widget-close-button';
  closeButton.src = 'BMW_close.png'; // Ensure the path is correct
  closeButton.alt = 'Close Chat';

  // Append elements to the header in order
  header.appendChild(logoImg); // Leftmost
  header.appendChild(headerText);
  header.appendChild(minimizeButton);
  header.appendChild(closeButton);

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

  widgetContainer.appendChild(inputContainer);

  // Privacy Overlay
  const privacyOverlay = document.createElement('div');
  privacyOverlay.id = 'chat-widget-privacy-overlay';

  // Privacy Content Container
  const privacyContent = document.createElement('div');
  privacyContent.id = 'chat-widget-privacy-content';

  // Privacy Text
  const privacyText = document.createElement('p');
  privacyText.id = 'chat-widget-privacy-text';
  privacyText.innerHTML =
    '<strong>Privacy Notice:</strong><br>' +
    'We value your privacy. The information you provide during this chat session will be used solely to assist you and improve our services. We do not share your personal data with third parties without your consent. For more details on how we handle your data, please read our <a href="your-privacy-policy-link" target="_blank">Privacy Policy</a>.<br><br>' +
    '<strong>Important Notice:</strong><br>' +
    'Our Virtual Assistant uses artificial intelligence to provide responses. While we strive for accuracy, the AI may occasionally provide incorrect or suboptimal information. Please verify any critical or sensitive information with official BMW sources or contact our customer support directly.<br><br>' +
    'By clicking "Accept," you acknowledge that you have read and agree to our Privacy Policy and understand the limitations of the AI assistant.';

  // Accept Button
  const acceptButton = document.createElement('button');
  acceptButton.id = 'chat-widget-privacy-accept-button';
  acceptButton.innerText = 'Accept';

  // Append elements
  privacyContent.appendChild(privacyText);
  privacyContent.appendChild(acceptButton);
  privacyOverlay.appendChild(privacyContent);

  // Append the privacy overlay to the widget container
  widgetContainer.appendChild(privacyOverlay);

  // Append the widget to the body (initially hidden)
  widgetContainer.style.display = 'none';
  document.body.appendChild(widgetContainer);

  // Include CSS file
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.type = 'text/css';
  link.href = 'chat-widget.css'; // Ensure the path is correct
  document.head.appendChild(link);

  // Disable input field initially
  inputField.disabled = true;

  // Function to open the chat
  function openChat() {
    isChatOpen = true;
    widgetContainer.style.display = 'flex';
    chatIcon.style.display = 'none';

    // Ensure chat components are visible
    chatHistory.style.display = 'flex';
    inputContainer.style.display = 'flex';

    if (!isPrivacyAccepted) {
      // Show the privacy overlay
      privacyOverlay.style.display = 'flex';
      // Disable the input field
      inputField.disabled = true;
    } else {
      // Hide the privacy overlay
      privacyOverlay.style.display = 'none';
      // Enable the input field
      inputField.disabled = false;
    }
  }

  // Function to minimize the chat
  function minimizeChat() {
    isChatOpen = false;
    widgetContainer.style.display = 'none';
    chatIcon.style.display = 'flex'; // Use 'flex' instead of 'block'
  }

  // Function to close and clear the chat
  function closeChat() {
    isChatOpen = false;
    widgetContainer.style.display = 'none';
    chatIcon.style.display = 'flex'; // Use 'flex' instead of 'block'
    // Clear the chat history
    chatHistory.innerHTML = '';
  }

  // Event listener for chat icon
  chatIcon.addEventListener('click', openChat);

  // Event listeners for minimize and close buttons
  minimizeButton.addEventListener('click', minimizeChat);
  closeButton.addEventListener('click', closeChat);

  // Event listener for accept button
  acceptButton.addEventListener('click', function () {
    isPrivacyAccepted = true;
    // Hide the privacy overlay
    privacyOverlay.style.display = 'none';
    // Enable the input field
    inputField.disabled = false;
    // Focus on the input field
    inputField.focus();
  });

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
        displayMessage(
          'bot',
          'Sorry, there was an error. Please try again later.'
        );
      });
  }

  // Event listener for input field
  inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      if (!isPrivacyAccepted) {
        // Do not allow sending messages until terms are accepted
        return;
      }
      sendMessage();
    }
  });
})();
