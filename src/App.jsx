import React from 'react'
import './App.css'
import mic from "./mic.png"
import MessageWindow from './MessageWindow'
import TextBar from './TextBar'
import { registerOnMessageCallback, send } from './websocket'

export class App extends React.Component {
  state = {
    messages: []
  };

  constructor (props) {
    super(props)
    registerOnMessageCallback(this.onMessageReceived.bind(this))
  }

  onMessageReceived (msg) {
    msg = JSON.parse(msg)
    this.setState((prevState) => ({
      messages: prevState.messages.concat(msg)
    }));
  }

  sendMessage (text) {
    if (text != '')
    {
    const message = {
      text: text
    }
    send(JSON.stringify(message))
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
