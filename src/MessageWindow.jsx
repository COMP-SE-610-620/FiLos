import React from 'react'
import './MessageWindow.css'

const Message = ({ text, self }) => (
  <div className={'message' + (self ? ' message-self' : '')}>    
    <div className='message-text'>{text}</div>
  </div>
)

export default class MessageWindow extends React.Component {
  constructor (props) {
    super(props)
    this.messageWindow = React.createRef()
  }
  componentDidUpdate () {
    const messageWindow = this.messageWindow.current
    messageWindow.scrollTop = messageWindow.scrollHeight - messageWindow.clientHeight
  }
  render () {
    const { messages = [] } = this.props
    return (
      <div className='message-window' ref={this.messageWindow}>
        {messages.map((msg, i) => {
          return <Message key={i} text={msg.text} self={msg.self} />
        })}
        <div>&nbsp;</div>
      </div>
    )
  }
}