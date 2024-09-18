// widget/chat-widget.js

(function () {
  // Configuration
  const apiUrl = 'http://127.0.0.1:5000/chat'; // Update with your backend URL

  // Flags to track the chat and privacy state
  let isChatOpen = false;
  let isPrivacyAccepted = false;
  let isChatStarted = false; // New flag to track if the chat has started
  let isSurveyOpen = false; // New flag to track if the survey is open

  // Create the minimized chat icon
  const chatIcon = document.createElement('div');
  chatIcon.id = 'chat-widget-icon';
  chatIcon.title = 'Apri Chat';

  // Create an image element for the chat icon
  const chatIconImg = document.createElement('img');
  chatIconImg.id = 'chat-widget-icon-img';
  chatIconImg.src = 'BMW_chat_icon.png'; // Ensure the path is correct
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
  logoImg.src = 'BMW_logo.png'; // Ensure the path is correct
  logoImg.alt = 'BMW Logo';

  // Add the header text
  const headerText = document.createElement('span');
  headerText.id = 'chat-widget-header-text';
  headerText.innerText = 'Assistente Virtuale';

  // Add the minimize button
  const minimizeButton = document.createElement('img');
  minimizeButton.id = 'chat-widget-minimize-button';
  minimizeButton.src = 'BMW_arrow_down.png'; // Ensure the path is correct
  minimizeButton.alt = 'Minimizza Chat';

  // Add the close button
  const closeButton = document.createElement('img');
  closeButton.id = 'chat-widget-close-button';
  closeButton.src = 'BMW_close.png'; // Ensure the path is correct
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
    "Il nostro Assistente Virtuale utilizza l'intelligenza artificiale per fornire risposte. Sebbene ci impegniamo per garantire l'accuratezza, l'AI potrebbe occasionalmente fornire informazioni inesatte o subottimali. Ti preghiamo di verificare informazioni critiche o sensibili con fonti ufficiali BMW o contattando direttamente il nostro servizio clienti.<br><br>" +
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
  link.href = 'chat-widget.css'; // Ensure the path is correct
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

    // Survey Text
    const surveyText = document.createElement('p');
    surveyText.id = 'chat-widget-survey-text';
    surveyText.innerHTML =
      'Il tuo feedback è importante per noi.<br>' +
      'Ti ringraziamo in anticipo se vorrai dedicarci qualche minuto del tuo tempo.<br><br>' +
      'La tua richiesta è stata risolta con un solo contatto?';

    // Survey Options
    const surveyOptions = document.createElement('div');
    surveyOptions.id = 'chat-widget-survey-options';

    const option1 = createSurveyOption('Sì', 'survey-option', true); // Radio button
    const option2 = createSurveyOption(
      'Sono stato informato sui tempi di gestione della mia richiesta',
      'survey-option',
      true
    );
    const option3 = createSurveyOption('No', 'survey-option', true);

    surveyOptions.appendChild(option1);
    surveyOptions.appendChild(option2);
    surveyOptions.appendChild(option3);

    // Second Question
    const surveyText2 = document.createElement('p');
    surveyText2.id = 'chat-widget-survey-text2';
    surveyText2.innerHTML =
      'Dopo questa tua esperienza, quanto raccomanderesti BMW Financial Services ad amici e colleghi, in una scala da 0 a 10?';

    // Rating Slider
    const ratingContainer = document.createElement('div');
    ratingContainer.id = 'chat-widget-rating-container';

    const ratingInput = document.createElement('input');
    ratingInput.type = 'range';
    ratingInput.min = '0';
    ratingInput.max = '10';
    ratingInput.step = '1'; // Ensure integer values
    ratingInput.id = 'chat-widget-rating-input';

    const ratingValue = document.createElement('span');
    ratingValue.id = 'chat-widget-rating-value';
    ratingValue.innerText = ''; // Start with no value

    ratingInput.addEventListener('input', function () {
      ratingValue.innerText = ratingInput.value;
    });

    ratingContainer.appendChild(ratingInput);
    ratingContainer.appendChild(ratingValue);

    // Final Question
    const surveyText3 = document.createElement('p');
    surveyText3.id = 'chat-widget-survey-text3';
    surveyText3.innerText =
      'Infine, per consentirci di migliorare la qualità del servizio, ti chiediamo di fornirci un tuo commento.';

    // Comments Textarea
    const commentsTextarea = document.createElement('textarea');
    commentsTextarea.id = 'chat-widget-comments-textarea';
    commentsTextarea.placeholder = 'Scrivi il tuo commento qui...';

    // Apply inline styles to ensure the textarea displays multiple lines
    commentsTextarea.style.width = '100%';
    commentsTextarea.style.height = '120px'; // Set desired height
    commentsTextarea.style.padding = '10px';
    commentsTextarea.style.fontSize = '14px';
    commentsTextarea.style.fontFamily = '"BMWType", Arial, Helvetica, sans-serif';
    commentsTextarea.style.marginBottom = '10px';
    commentsTextarea.style.border = '1px solid #ccc';
    commentsTextarea.style.borderRadius = '5px';
    commentsTextarea.style.resize = 'vertical';

    // Submit Button
    const submitButton = document.createElement('button');
    submitButton.id = 'chat-widget-survey-submit-button';
    submitButton.innerText = 'Invia';

    // Append elements to the survey container
    surveyContainer.appendChild(surveyText);
    surveyContainer.appendChild(surveyOptions);
    surveyContainer.appendChild(surveyText2);
    surveyContainer.appendChild(ratingContainer);
    surveyContainer.appendChild(surveyText3);
    surveyContainer.appendChild(commentsTextarea);
    surveyContainer.appendChild(submitButton);

    // Append the survey container to the main content
    mainContent.appendChild(surveyContainer);

    // Event listener for submit button
    submitButton.addEventListener('click', function () {
      // Collect survey data
      const selectedOption = surveyOptions.querySelector(
        '.chat-widget-survey-option input:checked'
      )?.value;

      const rating = ratingInput.value || null;
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

  // Helper function to create survey options
  function createSurveyOption(labelText, name, isRadio) {
    const optionLabel = document.createElement('label');
    optionLabel.classList.add('chat-widget-survey-option');

    const optionInput = document.createElement('input');
    optionInput.type = isRadio ? 'radio' : 'checkbox';
    optionInput.name = name;
    optionInput.value = labelText;

    const optionSpan = document.createElement('span');
    optionSpan.innerText = labelText;

    optionLabel.appendChild(optionInput);
    optionLabel.appendChild(optionSpan);

    return optionLabel;
  }
})();
