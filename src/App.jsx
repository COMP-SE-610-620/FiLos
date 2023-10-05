import React from 'react'
import './App.css'

import MessageWindow from './MessageWindow'
import TextBar from './TextBar'
import { registerOnMessageCallback, send } from './websocket'

export class App extends React.Component {
  state = {
    messages: []
  }

  constructor (props) {
    super(props)
    registerOnMessageCallback(this.onMessageReceived.bind(this))
  }

  onMessageReceived (msg) {
    msg = JSON.parse(msg)
    this.setState({
      messages: this.state.messages.concat(msg)
    })
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

  render () {
    const sendMessage = this.sendMessage.bind(this)
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

export default App
