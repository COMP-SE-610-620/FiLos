import React from 'react'
import './App.css'
import MessageWindow from './MessageWindow'
import TextBar from './TextBar'

export class App extends React.Component {
  state = {
    messages: [],
    isSelf: true
  };

  onNewMessage (msg) {
    msg = JSON.parse(msg)
    this.setState((prevState) => ({
      messages: prevState.messages.concat(msg)
    }));
  }  

  sendMessage (text) {
    if (text !== '')
    {
    const ourMessage = {
      text: text,
      self: true
    }
    this.onNewMessage(JSON.stringify(ourMessage));

    const formData = new FormData();
    formData.append("text_input", text);

    // POST to backend when a new message is sent
    fetch('http://localhost:8000/chat/text', {
      method: 'POST',
      body: formData,
      })
    .then(response => response.json())
    .then(data => {        
      console.log('Response from FiLOs:', data.response);
      const filosMessage = {
        text: data.response,
        self: false
      };
      this.onNewMessage(JSON.stringify(filosMessage));
    })
    .catch(error => {
      console.error('Error sending message:', error);
    });

  }
  }

  render() {
    const sendMessage = this.sendMessage.bind(this)

    if (this.state.messages.length === 0) {
      return (
        <>
        <TextBar onSend={sendMessage} landing={true}/>
        </>
      );
    } 
    else
    {
      return (
        <>                          
        <div className='container'>                
          <div className='container-title'>
            <b>FiLOS Test</b>
          </div>
          <div className='container-chat'>        
          <MessageWindow messages={this.state.messages} />        
          </div>
          <TextBar onSend={sendMessage}  landing={false}/>
        </div>
        </>
      )
    }
  }
}

export default App
