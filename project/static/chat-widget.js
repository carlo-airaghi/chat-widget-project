(function () {
    // Configuration
    const apiUrl = window.chatWidgetApiUrl || 'http://127.0.0.1:5000/chat';
    const baseUrl = window.chatWidgetBaseUrl || 'http://127.0.0.1:5000/static/';
  
    // Flags to track the chat and privacy state
    let isChatOpen = false;
    let isPrivacyAccepted = false;
    let isChatStarted = false; // Flag to track if the chat has started
    let isSurveyOpen = false; // Flag to track if the survey is open
  
    // Create the minimized chat icon
    const chatIcon = document.createElement('div');
    chatIcon.id = 'chat-widget-icon';
    chatIcon.title = 'Apri Chat';
  
    // Create an image element for the chat icon
    const chatIconImg = document.createElement('img');
    chatIconImg.id = 'chat-widget-icon-img';
    chatIconImg.src = baseUrl + 'images/BMW_chat_icon.png';
    chatIconImg.alt = 'Apri Chat';
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
    logoImg.src = baseUrl + 'images/theapeshape.PNG';
    logoImg.alt = 'Logo';
  
    // Add the header text
    const headerText = document.createElement('span');
    headerText.id = 'chat-widget-header-text';
    headerText.innerText = 'Coach Virtuale';
  
    // Add the minimize button
    const minimizeButton = document.createElement('img');
    minimizeButton.id = 'chat-widget-minimize-button';
    minimizeButton.src = baseUrl + 'images/BMW_arrow_down.png';
    minimizeButton.alt = 'Minimizza Chat';
  
    // Add the close button
    const closeButton = document.createElement('img');
    closeButton.id = 'chat-widget-close-button';
    closeButton.src = baseUrl + 'images/BMW_close.png';
    closeButton.alt = 'Chiudi Chat';
  
    // Append elements to the header in order
    header.appendChild(logoImg); // Leftmost
    header.appendChild(headerText);
    header.appendChild(minimizeButton);
    header.appendChild(closeButton);
  
    // Add the header to the widget container
    widgetContainer.appendChild(header);
  
    // Main content area (used to switch between chat, privacy form, and survey)
    const mainContent = document.createElement('div');
    mainContent.id = 'chat-widget-main-content';
  
    // Chat history
    const chatHistory = document.createElement('div');
    chatHistory.id = 'chat-widget-history';
    mainContent.appendChild(chatHistory);
  
    // Input container
    const inputContainer = document.createElement('div');
    inputContainer.id = 'chat-widget-input-container';
  
    const inputField = document.createElement('input');
    inputField.type = 'text';
    inputField.placeholder = 'Scrivi un messaggio...';
    inputField.id = 'chat-widget-input';
    inputContainer.appendChild(inputField);
  
    mainContent.appendChild(inputContainer);
  
    // Append the main content to the widget container
    widgetContainer.appendChild(mainContent);
  
    // Privacy Form Container
    const privacyContainer = document.createElement('div');
    privacyContainer.id = 'chat-widget-privacy-container';
  
    // Privacy Title
    const privacyTitle = document.createElement('h2');
    privacyTitle.id = 'chat-widget-privacy-title';
    privacyTitle.innerText = 'Informativa sulla Privacy';
  
    // Privacy Text
    const privacyText = document.createElement('p');
    privacyText.id = 'chat-widget-privacy-text';
    privacyText.innerHTML =
      'Le informazioni che fornirai durante questa sessione di chat saranno utilizzate esclusivamente per assisterti e migliorare i nostri servizi. Non condividiamo i tuoi dati personali con terze parti senza il tuo consenso. Per maggiori dettagli su come gestiamo i tuoi dati, ti preghiamo di leggere la nostra <a href="your-privacy-policy-link" target="_blank">Informativa sulla Privacy</a>.<br><br>' +
      '<strong>Avviso Importante:</strong><br>' +
      'Cliccando su "Accetto", confermi di aver letto e accettato la nostra Informativa sulla Privacy e di comprendere le limitazioni dell\'Assistente Virtuale.';
  
    // Accept Button
    const acceptButton = document.createElement('button');
    acceptButton.id = 'chat-widget-privacy-accept-button';
    acceptButton.innerText = 'Accetto';
  
    // Append elements
    privacyContainer.appendChild(privacyTitle);
    privacyContainer.appendChild(privacyText);
    privacyContainer.appendChild(acceptButton);
  
    // Append the privacy container to the main content
    mainContent.appendChild(privacyContainer);
  
    // Append the widget to the body (initially hidden)
    widgetContainer.style.display = 'none';
    document.body.appendChild(widgetContainer);
  
    // Include CSS file
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = baseUrl + 'chat-widget.css';
    document.head.appendChild(link);
  
    // Disable input field initially
    inputField.disabled = true;
  
    // Function to open the chat
    function openChat() {
      isChatOpen = true;
      widgetContainer.style.display = 'flex';
      chatIcon.style.display = 'none';
  
      if (!isPrivacyAccepted) {
        // Show the privacy form
        privacyContainer.style.display = 'flex';
        chatHistory.style.display = 'none';
        inputContainer.style.display = 'none';
      } else {
        // Show the chat components
        privacyContainer.style.display = 'none';
        chatHistory.style.display = 'flex';
        inputContainer.style.display = 'flex';
        inputField.disabled = false;
      }
    }
  
    // Function to minimize the chat
    function minimizeChat() {
      isChatOpen = false;
      widgetContainer.style.display = 'none';
      chatIcon.style.display = 'flex';
    }
  
    // Function to close and clear the chat, then conditionally show the survey
    function closeChat() {
      isChatOpen = false;
  
      if (isSurveyOpen) {
        // If the survey is already open, just close the widget
        widgetContainer.style.display = 'none';
        chatIcon.style.display = 'flex';
        isSurveyOpen = false; // Reset the flag
  
        // Remove the survey container if it exists
        const surveyContainer = document.getElementById('chat-widget-survey-container');
        if (surveyContainer) {
          surveyContainer.remove();
        }
  
        // Reset the chat for next use
        chatHistory.innerHTML = '';
        inputField.value = '';
        isChatStarted = false;
      } else if (isChatStarted) {
        // If the chat has started, show the survey
        // Clear the chat history and input
        chatHistory.innerHTML = '';
        inputField.value = '';
  
        // Show the survey within the chat widget
        showSurvey();
      } else {
        // If the chat hasn't started, just close the widget
        widgetContainer.style.display = 'none';
        chatIcon.style.display = 'flex';
  
        // Reset the chat for next use
        chatHistory.innerHTML = '';
        inputField.value = '';
        privacyContainer.style.display = 'none';
        chatHistory.style.display = 'flex';
        inputContainer.style.display = 'flex';
      }
    }
  
    // Event listener for chat icon
    chatIcon.addEventListener('click', openChat);
  
    // Event listeners for minimize and close buttons
    minimizeButton.addEventListener('click', minimizeChat);
    closeButton.addEventListener('click', closeChat);
  
    // Function to display a welcome message
    function displayWelcomeMessage() {
      const welcomeMessage = "Ciao! Sono il tuo coach virtuale. Come posso aiutarti oggi?";
      displayMessage('bot', welcomeMessage);
    }
  
    // Event listener for accept button
    acceptButton.addEventListener('click', function () {
      isPrivacyAccepted = true;
      // Hide the privacy container
      privacyContainer.style.display = 'none';
      // Show chat components
      chatHistory.style.display = 'flex';
      inputContainer.style.display = 'flex';
      // Enable the input field
      inputField.disabled = false;
      // Focus on the input field
      inputField.focus();
      // Display the welcome message
      displayWelcomeMessage();
    });
  
    // Function to display messages with improved scroll management
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
        const containerHeight = chatHistory.clientHeight;
  
        // Scroll to the new message smoothly
        chatHistory.scrollTo({
          top: messageTop - containerHeight / 3,
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
  
      // Mark the chat as started
      isChatStarted = true;
  
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
            displayMessage('bot', 'Spiacenti, si è verificato un errore.');
          }
        })
        .catch((error) => {
          console.error('Error:', error);
          displayMessage(
            'bot',
            'Spiacenti, si è verificato un errore. Per favore riprova più tardi.'
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
  
    // Function to show the survey within the chat widget
    function showSurvey() {
      isSurveyOpen = true;
  
      // Show the chat widget
      widgetContainer.style.display = 'flex';
      chatIcon.style.display = 'none';
  
      // Clear the chat history and hide input container
      chatHistory.innerHTML = '';
      chatHistory.style.display = 'none';
      inputContainer.style.display = 'none';
  
      // Create the survey container
      const surveyContainer = document.createElement('div');
      surveyContainer.id = 'chat-widget-survey-container';
  
      // First Question
      const surveyQuestion1 = document.createElement('p');
      surveyQuestion1.id = 'chat-widget-survey-question1';
      surveyQuestion1.innerText =
        'In una scala da 1 a 10, quanto ti hanno soddisfatto le risposte ricevute?';
  
      // Rating Slider for Question 1
      const ratingContainer1 = document.createElement('div');
      ratingContainer1.className = 'chat-widget-rating-container';
  
      const ratingInput1 = document.createElement('input');
      ratingInput1.type = 'range';
      ratingInput1.min = '1';
      ratingInput1.max = '10';
      ratingInput1.step = '1';
      ratingInput1.className = 'chat-widget-rating-input';
  
      const ratingValue1 = document.createElement('span');
      ratingValue1.className = 'chat-widget-rating-value';
      ratingValue1.innerText = ''; // Start with no value
  
      ratingInput1.addEventListener('input', function () {
        ratingValue1.innerText = ratingInput1.value;
      });
  
      ratingContainer1.appendChild(ratingInput1);
      ratingContainer1.appendChild(ratingValue1);
  
      // Second Question
      const surveyQuestion2 = document.createElement('p');
      surveyQuestion2.id = 'chat-widget-survey-question2';
      surveyQuestion2.innerText =
        "In una scala da 1 a 10, quanto consiglieresti l'app ad amici e colleghi?";
  
      // Rating Slider for Question 2
      const ratingContainer2 = document.createElement('div');
      ratingContainer2.className = 'chat-widget-rating-container';
  
      const ratingInput2 = document.createElement('input');
      ratingInput2.type = 'range';
      ratingInput2.min = '1';
      ratingInput2.max = '10';
      ratingInput2.step = '1';
      ratingInput2.className = 'chat-widget-rating-input';
  
      const ratingValue2 = document.createElement('span');
      ratingValue2.className = 'chat-widget-rating-value';
      ratingValue2.innerText = ''; // Start with no value
  
      ratingInput2.addEventListener('input', function () {
        ratingValue2.innerText = ratingInput2.value;
      });
  
      ratingContainer2.appendChild(ratingInput2);
      ratingContainer2.appendChild(ratingValue2);
  
      // Third Question (Free-text Input)
      const surveyQuestion3 = document.createElement('p');
      surveyQuestion3.id = 'chat-widget-survey-question3';
      surveyQuestion3.innerText = 'Cosa consiglieresti per migliorare il servizio?';
  
      // Comments Textarea
      const commentsTextarea = document.createElement('textarea');
      commentsTextarea.id = 'chat-widget-comments-textarea';
      commentsTextarea.placeholder = 'Scrivi il tuo commento qui...';
  
      // Apply inline styles to ensure the textarea displays multiple lines
      commentsTextarea.style.width = '100%';
      commentsTextarea.style.height = '100px';
      commentsTextarea.style.padding = '10px';
      commentsTextarea.style.fontSize = '14px';
      commentsTextarea.style.fontFamily = '"Area", Arial, Helvetica, sans-serif';
      commentsTextarea.style.marginBottom = '10px';
      commentsTextarea.style.border = '1px solid #ccc';
      commentsTextarea.style.borderRadius = '5px';
      commentsTextarea.style.resize = 'vertical';
  
      // Submit Button
      const submitButton = document.createElement('button');
      submitButton.id = 'chat-widget-survey-submit-button';
      submitButton.innerText = 'Invia';
  
      // Append elements to the survey container
      surveyContainer.appendChild(surveyQuestion1);
      surveyContainer.appendChild(ratingContainer1);
      surveyContainer.appendChild(surveyQuestion2);
      surveyContainer.appendChild(ratingContainer2);
      surveyContainer.appendChild(surveyQuestion3);
      surveyContainer.appendChild(commentsTextarea);
      surveyContainer.appendChild(submitButton);
  
      // Append the survey container to the main content
      mainContent.appendChild(surveyContainer);
  
      // Event listener for submit button
      submitButton.addEventListener('click', function () {
        // Collect survey data
        const satisfactionRating = ratingInput1.value || null;
        const recommendationRating = ratingInput2.value || null;
        const comments = commentsTextarea.value.trim();
  
        // Here, you can send the survey data to your server if needed
  
        // Close the chat widget
        widgetContainer.style.display = 'none';
        chatIcon.style.display = 'flex';
  
        // Reset the chat widget for next use
        surveyContainer.remove();
        chatHistory.innerHTML = '';
        inputContainer.style.display = 'flex';
        chatHistory.style.display = 'flex';
  
        // Reset flags
        isSurveyOpen = false;
        isChatStarted = false;
      });
    }
  })();
  