window.chatbot = {
  init: function () {
    window.chatbot.serverUrl = window.chatbot.serverUrl || '';
  },
};

class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector('.chatbox__button'),
      chatBox: document.querySelector('.chatbox__support'),
      sendButton: document.querySelector('.send__button'),
    };

    this.state = false;
    this.messages = [];
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener('click', () =>
      this.toggleState(chatBox)
    );
    sendButton.addEventListener('click', () =>
      this.onSendButton(chatBox)
    );
    const node = chatBox.querySelector('input');
    node.addEventListener('keyup', ({ key }) => {
      if (key === 'Enter') {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatBox) {
    this.state = !this.state;

    if (this.state) {
      chatBox.classList.add('chatbox--active');
    } else {
      chatBox.classList.remove('chatbox--active');
    }
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector('input');
    let text1 = textField.value;
    if (text1 === '') {
      return;
    }

    let msg1 = { name: 'User', message: text1 };
    this.messages.push(msg1);

    fetch(window.chatbot.serverUrl + '/predict', {
      method: 'POST',
      body: JSON.stringify({
        message: text1,
        user_id: window.chatbot.userId,
      }),
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: 'Botberto', message: r.response };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = '';
      })
      .catch((error) => {
        console.error('Error:', error);
        this.updateChatText(chatbox);
        textField.value = '';
      });
  }

  updateChatText(chatbox) {
    var html = '';
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (item.name === 'Botberto') {
          html +=
            '<div class="messages__item messages__item--visitor">' +
            item.message +
            '</div>';
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            '</div>';
        }
      });

    const chatmessage = chatbox.querySelector('.chatbox__messages');
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();
window.chatbot.init();