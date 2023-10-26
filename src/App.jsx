import React from 'react'
import './App.css'
import mic from "./mic.png"
import MessageWindow from './MessageWindow'
import TextBar from './TextBar'
import { registerOnMessageCallback, send } from './websocket'

export class App extends React.Component {
  state = {
    messages: [],
    showLandingPage: true, // change between landing page and chat
  };

  constructor (props) {
    super(props)
    registerOnMessageCallback(this.onMessageReceived.bind(this))
  }

  onMessageReceived (msg) {
    msg = JSON.parse(msg)
    this.setState((prevState) => ({
      messages: prevState.messages.concat(msg),
      showLandingPage: false, // tried to make this change the page but it didn't work
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

    if (this.state.showLandingPage) {
      return (
        <div className='container-landing'>
            <img src='FiLOS.png' width="200"></img>
            <h1>Welcome to FiLOs!</h1>
            <p>Your Finnish AI assistant.</p>
            <p></p>
            <div className='textbar-landing'>
              <input placeholder='Enter your message here...' className='textbar-input' type='text' ref={this.input} />
              
            </div>
            <p><b>or</b></p>
            <div className='mic'>
              <button className='textbar-send' onClick={sendMessage}>
              <img src={mic} width={70} height={70}/>
              </button>
            </div>
            <p>Speak with FiLOs</p>
        </div>
      );
    } 
    
    else {
      return (
        <>                  
        <div className='container'>        
          <div className='container-title'>
            <b>FiLOS Test</b>
          </div>
          <div className='container-chat'>        
          <MessageWindow messages={this.state.messages} />        
          </div>
          <TextBar onSend={sendMessage} />
        </div>
        </>
      )
    }
  }
}

export default App
