import React, { useState } from 'react';
import './TextBar.css';
import mic from './mic.png';
import play from "./play.png";

const VoiceRecorder = ({ sendingMessage }) => {
  const [audioStream, setAudioStream] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recording, setRecording] = useState(false);
  const [audioChunks, setAudioChunks] = useState([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioStream(stream);
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' }); // Specify MIME type
      setMediaRecorder(recorder);

      recorder.ondataavailable = (e) => {
        setAudioChunks((chunks) => [...chunks, e.data]);
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.webm');
      
        fetch('http://localhost:8000/chat/speech', {
          method: 'POST',
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          console.log('Response from FiLOs:', data.response);
          sendingMessage(JSON.stringify(data.response));
        })
        .catch(error => {
          console.error('Error sending message:', error);
        });
      };
      recorder.start();
      setRecording(true);
    } catch (error) {
      console.error('Error accessing the microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
      setRecording(false);
      audioStream.getTracks().forEach(track => track.stop());
    }
  };

  return (
    <button className='textbar-mic' onClick={recording ? stopRecording : startRecording}>
      {recording ? (
        <img src={play} width={40} height={40} alt="Stop Recording" />
      ) : (
        <img src={mic} width={40} height={40} alt="Start Recording" />
      )}
    </button>
  );
};

class TextBar extends React.Component {
  constructor(props) {
    super(props);
    this.input = React.createRef();
  }

  sendMessage(prompt) {
    this.props.onSend && this.props.onSend(prompt);
    this.input.current.value = '';
  }

  sendMessageIfEnter = (e) => {
    if (e.keyCode === 13) {
      this.sendMessage(this.input.current.value);
    }
  };

  render() {
    if (this.props.landing) {
      return (
        <div className='container'>
          <br/><br/>
          <img src='FiLOS.png' width="200" alt="FiLOS logo"></img>
          <h1>Welcome to FiLOs!</h1>
          Your Finnish AI assistant.
          <br/><br/>
          <div>
            <input
              placeholder='Enter your message here...'
              className='textbar-input'
              type='text'
              ref={this.input}
              onKeyDown={this.sendMessageIfEnter}
            />
          </div>
          <p><b>or</b></p>
          <VoiceRecorder sendingMessage={this.sendMessage}/>
          <p>Speak with FiLOs</p>
        </div>
      );
    } else {
      return (
        <div className='container-textbar'>
          <div className='textbar'>
            <input
              placeholder='Enter your message here...'
              className='textbar-input'
              type='text'
              ref={this.input}
              onKeyDown={this.sendMessageIfEnter}
            />
            <VoiceRecorder sendingMessage={this.sendMessage}/>
          </div>
        </div>
      );
    }
  }
}

export default TextBar;
