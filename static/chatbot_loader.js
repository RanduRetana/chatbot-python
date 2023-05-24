(function () {
  function injectChatbotHTML() {
    const botName = window.chatbotName || 'Botberto';
    const chatbotHTML = `
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-PJMGVXW');</script>
    <!-- End Google Tag Manager -->
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PJMGVXW"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->
      <div class="container">
        <div class="chatbox">
          <div class="chatbox__support">
            <div class="chatbox__header">
              <div class="chatbox__image--header">
                <img src="https://convierto.uc.r.appspot.com/static/images/logo.svg" alt="image">
              </div>
              <div class="chatbox__content--header">
                <h4 class="chatbox__heading--header">Tu amigo ${botName}</h4>
                <p class="chatbox__description--header">Platica con ${botName}!</p>
              </div>
            </div>
            <div class="chatbox__messages">
              <div></div>
            </div>
            <div class="chatbox__footer">
              <input type="text" placeholder="Write a message...">
              <button class="chatbox__send--footer send__button">Send</button>
            </div>
          </div>
          <div class="chatbox__button">
            <button><img src="/static/images/chatbox-icon.svg" /></button>
          </div>
        </div>
      </div>`;
    document.body.insertAdjacentHTML('beforeend', chatbotHTML);
  }

  function loadStylesheet(url) {
    var link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = url;
    document.head.appendChild(link);
  }

  function loadScript(url, callback) {
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.async = true;
    script.onload = callback;
    document.head.appendChild(script);
  }

  function initializeChatbot() {
    var chatbotUrl = 'https://convierto.uc.r.appspot.com/'; // Reemplaza esto con la URL de tu servidor Flask.

    injectChatbotHTML();
    loadStylesheet(chatbotUrl + '/static/styles.css');

    // Agrega esta línea para pasar el ID del usuario al objeto chatbot
    window.chatbotUserId =
      typeof chatbotUserId !== 'undefined' ? chatbotUserId : null;

    // window.chatbot.empresaName =
    //   typeof window.empresaName !== 'undefined'
    //     ? window.empresaName
    //     : null;

    loadScript(chatbotUrl + '/static/app.js', function () {
      // Asegúrate de que app.js esté configurado para trabajar con la URL de tu servidor Flask.
      window.chatbot.serverUrl = chatbotUrl;
    });
  }

  initializeChatbot();
})();
