class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }
        // Chatbox open or close 
        this.state = false;
        // Store user message 
        this.messages = [];

    }

    display(){
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if(key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatBox) {
        this.state = !this.state;

        // show or hide the chat box 

        if(this.state)  {
            chatBox.classList.add('chatbox--active')
        }else{
            chatBox.classList.remove('chatbox--active')
        }

    }

    onSendButton(chatBox) {
        // extract user input text
        var textField = chatBox.querySelector('input');
        let text1 = textField.value;

        // if user enters nothing
        if (text1 === "") {
            return;
        }

        let msg1 = {name: "User", message: text1}
        this.messages.push(msg1)

        // In Base.html but can be hard coded to http://127.0.0.1:5000/predict 
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({message: text1}),
            mode: 'cors',
            headers: {
                'Content-Type' : 'application/json'
              },
        })
        .then(r => r.json())
        .then(r => {
            // Display back to the user 
            let msg2 = {name: "Ralph", message: r.answer};
            this.messages.push(msg2);
            this.updateChatText(chatBox);
            textField.value = ''

        }).catch((error) => {
            console.error('Error:' , error);
            this.updateChatText(chatBox);
            textField.value = '';
        });

    }

    updateChatText(chatBox){
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if(item.name === "Ralph")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }else{
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });

        const chatmessage = chatBox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

}

const chatbox = new Chatbox();
chatbox.display();