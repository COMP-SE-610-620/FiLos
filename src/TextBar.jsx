import React, { useState } from 'react';
import './TextBar.css';
import mic from './mic.png';
import play from "./play.png";

const VoiceRecorder = ({ sendingMessage, handleFileUpload }) => {
  const [audioStream, setAudioStream] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recording, setRecording] = useState(false);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioStream(stream);
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });   
      let chunks = [];   
      let audioElement;

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      recorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' }); // Change type to 'audio/wav'
        console.log('Recorded Blob:', audioBlob);
      
        // // Create a Blob URL and set it as the source for the Audio element
        // const audioUrl = URL.createObjectURL(audioBlob);
        // const audioElement = new Audio(audioUrl);
        // audioElement.src = audioUrl;
      
        // // Play the recorded audio
        // audioElement.play();
      
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav'); // Change field name to 'audio' and filename to 'audio.wav'
      
        fetch('http://localhost:8000/chat/speech', {
          method: 'POST',
          body: formData,
        })
        .then(response => response.json())
        .then(data => {
          console.log('Response from FiLOs:', data.response);
          sendingMessage(data.response + "?");
        })
        .catch(error => {
          console.error('Error sending message:', error);
        });
      };
      
      setMediaRecorder(recorder);
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
    <div>
      <input
        type="file"
        accept="audio/*"
        style={{ display: 'none' }}
        onChange={handleFileUpload}
        id="fileInput"
      />
      <button className='textbar-mic' onClick={recording ? stopRecording : startRecording}>
        {recording ? (
          <img src={play} width={40} height={40} alt="Stop Recording" />
        ) : (
          <img src={mic} width={40} height={40} alt="Start Recording" />
        )}
      </button>
      <button onClick={() => document.getElementById('fileInput').click()}>
        Upload Audio
      </button>
    </div>
  );
};

class TextBar extends React.Component {
  constructor(props) {
    super(props);
    this.input = React.createRef();
    this.sendMessage = this.sendMessage.bind(this);
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

  handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const formData = new FormData();
      // Use the correct field name ('audio') and content type
      formData.append('audio', file, { filename: 'audio.wav', type: 'audio/wav' });
  
      fetch('http://localhost:8000/chat/speech', {
          method: 'POST',
        body: formData,
      })
      .then(response => response.json())
      .then(data => {
        console.log('Response from FiLOs:', data.response);
        this.sendMessage(data.response + "?");
      })
      .catch(error => {
        console.error('Error sending message:', error);
      });
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
          <VoiceRecorder sendingMessage={this.sendMessage} handleFileUpload={this.handleFileUpload} />
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
            <VoiceRecorder sendingMessage={this.sendMessage} handleFileUpload={this.handleFileUpload} />
          </div>
        </div>
      );
    }
  }
}

export default TextBar;
