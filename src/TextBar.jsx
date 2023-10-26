import React, { Component } from 'react'
import './TextBar.css'
import mic from "./mic.png"

export default class TextBar extends Component {
  constructor (props) {
    super(props)
    this.input = React.createRef()
  }
  sendMessage () {
    this.props.onSend && this.props.onSend(this.input.current.value)
    this.input.current.value = ''
  }
  sendMessageIfEnter (e) {
    if (e.keyCode === 13) {
      this.sendMessage()
    }
  }
  render () {
    const sendMessage = this.sendMessage.bind(this)
    const sendMessageIfEnter = this.sendMessageIfEnter.bind(this)
    if (this.props.landing)
    {
    return (
        <div className='container'>        
        <br/><br/>
        <img src='FiLOS.png' width="200"></img>
            <h1>Welcome to FiLOs!</h1>
            Your Finnish AI assistant.
            <br/><br/>
            <div>
            <input placeholder='Enter your message here...' className='textbar-input' type='text' ref={this.input} onKeyDown={sendMessageIfEnter} />
            </div>
            <p><b>or</b></p>
            <button className='textbar-send-landing' onClick={sendMessage}>
            <img src={mic} width={70} height={70}/>
            </button>
            <p>Speak with FiLOs</p>
        </div>
    )
    }
    else
    {      
        return (
          <div className='container-textbar'>        
          <div className='textbar'>
            <input placeholder='Enter your message here...' className='textbar-input' type='text' ref={this.input} onKeyDown={sendMessageIfEnter} />
            <button className='textbar-send' onClick={sendMessage}>
            <img src={mic} width={40} height={40}/>
            </button>
          </div>
          </div>
      )
    }
  }
}