(function () {
  // Configuration
  const apiUrl = window.chatWidgetApiUrl || 'http://127.0.0.1:5000/chat';
  const baseUrl = window.chatWidgetBaseUrl || 'http://127.0.0.1:5000/static/';

  // Recupera i dati dell'utente da variabili globali o come preferisci
  const customerID = window.customer_id || null;
  const customerName = window.customerName || '';
  const customerSurname = window.customerSurname || '';
  const customerAge = window.customerAge || null;
  const customerSesso = window.customerSesso || '';
  const customerWeight = window.customerWeight || null;
  const customerHeight = window.customerHeight || null;
  const customerPercentualeMassaGrassa = window.customerPercentualeMassaGrassa || null;
  const customerDispendioCalorico = window.customerDispendioCalorico || null;
  const customerDietType = window.customerDietType || null;
  const customerMacroFase = window.customerMacroFase || null;
  const customerWeek = window.customerWeek || null;
  const customerDay = window.customerDay || null;
  const customerDistrettoCarente1 = window.customerDistrettoCarente1 || '';
  const customerDistrettoCarente2 = window.customerDistrettoCarente2 || '';
  const customerExerciseSelected = window.customerExerciseSelected || false;
  const customerContry = window.customerContry || '';
  const customerCity = window.customerCity || '';
  const customerProvince = window.customerProvince || '';
  const customerSubExpire = window.customerSubExpire || '';
  const customerSubType = window.customerSubType || null;

  // Flags
  let isChatOpen = false;
  let isPrivacyAccepted = false;
  let isChatStarted = false;
  let isSurveyOpen = false;

  // Crea l'icona minimizzata
  const chatIcon = document.createElement('div');
  chatIcon.id = 'chat-widget-icon';
  chatIcon.title = 'Apri Chat';

  const chatIconImg = document.createElement('img');
  chatIconImg.id = 'chat-widget-icon-img';
  chatIconImg.src = baseUrl + 'images/BMW_chat_icon.png';
  chatIconImg.alt = 'Apri Chat';
  chatIcon.appendChild(chatIconImg);

  document.body.appendChild(chatIcon);

  // Crea il container principale
  const widgetContainer = document.createElement('div');
  widgetContainer.id = 'chat-widget-container';

  // Header
  const header = document.createElement('div');
  header.id = 'chat-widget-header';

  const logoImg = document.createElement('img');
  logoImg.id = 'chat-widget-logo';
  logoImg.src = baseUrl + 'images/theapeshape.PNG';
  logoImg.alt = 'Logo';

  const headerText = document.createElement('span');
  headerText.id = 'chat-widget-header-text';
  headerText.innerText = 'Coach Virtuale';

  const minimizeButton = document.createElement('img');
  minimizeButton.id = 'chat-widget-minimize-button';
  minimizeButton.src = baseUrl + 'images/BMW_arrow_down.png';
  minimizeButton.alt = 'Minimizza Chat';

  const closeButton = document.createElement('img');
  closeButton.id = 'chat-widget-close-button';
  closeButton.src = baseUrl + 'images/BMW_close.png';
  closeButton.alt = 'Chiudi Chat';

  header.appendChild(logoImg);
  header.appendChild(headerText);
  header.appendChild(minimizeButton);
  header.appendChild(closeButton);

  widgetContainer.appendChild(header);

  // Main content
  const mainContent = document.createElement('div');
  mainContent.id = 'chat-widget-main-content';

  const chatHistory = document.createElement('div');
  chatHistory.id = 'chat-widget-history';
  mainContent.appendChild(chatHistory);

  const inputContainer = document.createElement('div');
  inputContainer.id = 'chat-widget-input-container';

  const inputField = document.createElement('input');
  inputField.type = 'text';
  inputField.placeholder = 'Scrivi un messaggio...';
  inputField.id = 'chat-widget-input';
  inputContainer.appendChild(inputField);

  mainContent.appendChild(inputContainer);
  widgetContainer.appendChild(mainContent);

  // Privacy Container
  const privacyContainer = document.createElement('div');
  privacyContainer.id = 'chat-widget-privacy-container';

  const privacyTitle = document.createElement('h2');
  privacyTitle.id = 'chat-widget-privacy-title';
  privacyTitle.innerText = 'Informativa sulla Privacy';

  const privacyText = document.createElement('p');
  privacyText.id = 'chat-widget-privacy-text';
  privacyText.innerHTML =
    'Le informazioni che fornirai durante questa sessione di chat saranno utilizzate esclusivamente per assisterti e migliorare i nostri servizi. ' +
    'Non condividiamo i tuoi dati personali con terze parti senza il tuo consenso. ' +
    'Per maggiori dettagli su come gestiamo i tuoi dati, ti preghiamo di leggere la nostra ' +
    '<a href="your-privacy-policy-link" target="_blank">Informativa sulla Privacy</a>.<br><br>' +
    '<strong>Avviso Importante:</strong><br>' +
    'Cliccando su "Accetto", confermi di aver letto e accettato la nostra Informativa sulla Privacy e di comprendere le limitazioni dell\'Assistente Virtuale.';

  const acceptButton = document.createElement('button');
  acceptButton.id = 'chat-widget-privacy-accept-button';
  acceptButton.innerText = 'Accetto';

  privacyContainer.appendChild(privacyTitle);
  privacyContainer.appendChild(privacyText);
  privacyContainer.appendChild(acceptButton);
  mainContent.appendChild(privacyContainer);

  widgetContainer.style.display = 'none';
  document.body.appendChild(widgetContainer);

  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.type = 'text/css';
  link.href = baseUrl + 'chat-widget.css';
  document.head.appendChild(link);

  inputField.disabled = true;

  // Funzioni
  function openChat() {
    isChatOpen = true;
    widgetContainer.style.display = 'flex';
    chatIcon.style.display = 'none';

    if (!isPrivacyAccepted) {
      privacyContainer.style.display = 'flex';
      chatHistory.style.display = 'none';
      inputContainer.style.display = 'none';
    } else {
      privacyContainer.style.display = 'none';
      chatHistory.style.display = 'flex';
      inputContainer.style.display = 'flex';
      inputField.disabled = false;
    }
  }

  function minimizeChat() {
    isChatOpen = false;
    widgetContainer.style.display = 'none';
    chatIcon.style.display = 'flex';
  }

  function closeChat() {
    isChatOpen = false;

    if (isSurveyOpen) {
      widgetContainer.style.display = 'none';
      chatIcon.style.display = 'flex';
      isSurveyOpen = false; 
      const surveyContainer = document.getElementById('chat-widget-survey-container');
      if (surveyContainer) {
        surveyContainer.remove();
      }
      chatHistory.innerHTML = '';
      inputField.value = '';
      isChatStarted = false;
    } else if (isChatStarted) {
      chatHistory.innerHTML = '';
      inputField.value = '';
      showSurvey();
    } else {
      widgetContainer.style.display = 'none';
      chatIcon.style.display = 'flex';
      chatHistory.innerHTML = '';
      inputField.value = '';
      privacyContainer.style.display = 'none';
      chatHistory.style.display = 'flex';
      inputContainer.style.display = 'flex';
    }
  }

  chatIcon.addEventListener('click', openChat);
  minimizeButton.addEventListener('click', minimizeChat);
  closeButton.addEventListener('click', closeChat);

  function displayWelcomeMessage() {
    const welcomeMessage = `Ciao ${customerName}! Sono il tuo coach virtuale. Come posso aiutarti oggi?`;
    displayMessage('bot', welcomeMessage);
  }

  acceptButton.addEventListener('click', function () {
    isPrivacyAccepted = true;
    privacyContainer.style.display = 'none';
    chatHistory.style.display = 'flex';
    inputContainer.style.display = 'flex';
    inputField.disabled = false;
    inputField.focus();
    displayWelcomeMessage();
  });

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

    setTimeout(() => {
      const messageTop = messageContainer.offsetTop;
      const containerHeight = chatHistory.clientHeight;
      chatHistory.scrollTo({
        top: messageTop - containerHeight / 3,
        behavior: 'smooth',
      });
    }, 0);
  }

  function sendMessage() {
    const message = inputField.value.trim();
    if (message === '') return;

    displayMessage('user', message);
    inputField.value = '';

    isChatStarted = true;

    // Qui costruiamo il JSON da mandare al backend
    const payload = {
      message: message,
      user: {
        Customer_ID: customerID,
        Name: customerName,
        Surname: customerSurname,
        Age: customerAge,
        Sesso: customerSesso,
        Weight: customerWeight,
        Height: customerHeight,
        PercentualeMassaGrassa: customerPercentualeMassaGrassa,
        DispendioCalorico: customerDispendioCalorico,
        DietType: customerDietType,
        MacroFase: customerMacroFase,
        Week: customerWeek,
        Day: customerDay,
        DistrettoCarente1: customerDistrettoCarente1,
        DistrettoCarente2: customerDistrettoCarente2,
        ExerciseSelected: customerExerciseSelected,
        Contry: customerContry,
        City: customerCity,
        Province: customerProvince,
        subExpire: customerSubExpire,
        SubType: customerSubType
      }
    };

    // Esegui la fetch
    fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
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

  inputField.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      if (!isPrivacyAccepted) {
        return;
      }
      sendMessage();
    }
  });

  function showSurvey() {
    isSurveyOpen = true;
    widgetContainer.style.display = 'flex';
    chatIcon.style.display = 'none';
    chatHistory.innerHTML = '';
    chatHistory.style.display = 'none';
    inputContainer.style.display = 'none';

    const surveyContainer = document.createElement('div');
    surveyContainer.id = 'chat-widget-survey-container';

    const surveyQuestion1 = document.createElement('p');
    surveyQuestion1.id = 'chat-widget-survey-question1';
    surveyQuestion1.innerText =
      'In una scala da 1 a 10, quanto ti hanno soddisfatto le risposte ricevute?';

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
    ratingValue1.innerText = '';

    ratingInput1.addEventListener('input', function () {
      ratingValue1.innerText = ratingInput1.value;
    });

    ratingContainer1.appendChild(ratingInput1);
    ratingContainer1.appendChild(ratingValue1);

    const surveyQuestion2 = document.createElement('p');
    surveyQuestion2.id = 'chat-widget-survey-question2';
    surveyQuestion2.innerText =
      "In una scala da 1 a 10, quanto consiglieresti l'app ad amici e colleghi?";

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
    ratingValue2.innerText = '';

    ratingInput2.addEventListener('input', function () {
      ratingValue2.innerText = ratingInput2.value;
    });

    ratingContainer2.appendChild(ratingInput2);
    ratingContainer2.appendChild(ratingValue2);

    const surveyQuestion3 = document.createElement('p');
    surveyQuestion3.id = 'chat-widget-survey-question3';
    surveyQuestion3.innerText = 'Cosa consiglieresti per migliorare il servizio?';

    const commentsTextarea = document.createElement('textarea');
    commentsTextarea.id = 'chat-widget-comments-textarea';
    commentsTextarea.placeholder = 'Scrivi il tuo commento qui...';

    commentsTextarea.style.width = '100%';
    commentsTextarea.style.height = '100px';
    commentsTextarea.style.padding = '10px';
    commentsTextarea.style.fontSize = '14px';
    commentsTextarea.style.fontFamily = '"Area", Arial, Helvetica, sans-serif';
    commentsTextarea.style.marginBottom = '10px';
    commentsTextarea.style.border = '1px solid #ccc';
    commentsTextarea.style.borderRadius = '5px';
    commentsTextarea.style.resize = 'vertical';

    const submitButton = document.createElement('button');
    submitButton.id = 'chat-widget-survey-submit-button';
    submitButton.innerText = 'Invia';

    surveyContainer.appendChild(surveyQuestion1);
    surveyContainer.appendChild(ratingContainer1);
    surveyContainer.appendChild(surveyQuestion2);
    surveyContainer.appendChild(ratingContainer2);
    surveyContainer.appendChild(surveyQuestion3);
    surveyContainer.appendChild(commentsTextarea);
    surveyContainer.appendChild(submitButton);

    mainContent.appendChild(surveyContainer);

    submitButton.addEventListener('click', function () {
      const satisfactionRating = ratingInput1.value || null;
      const recommendationRating = ratingInput2.value || null;
      const comments = commentsTextarea.value.trim();

      // Se vuoi inviare i dati del questionario ad un endpoint, puoi farlo qui

      widgetContainer.style.display = 'none';
      chatIcon.style.display = 'flex';

      surveyContainer.remove();
      chatHistory.innerHTML = '';
      inputContainer.style.display = 'flex';
      chatHistory.style.display = 'flex';

      isSurveyOpen = false;
      isChatStarted = false;
    });
  }
})();
