import React, { useState } from 'react';
import './MessageWindow.css';
import play from "./play.png";
import stop from "./stop.png";
let source;

const Message = ({ text, self }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const playAudio = (buffer) => {
    const audioContext = new AudioContext();
    source = audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(audioContext.destination);    
    source.start(0);
    source.onended = () => {
      setIsPlaying(false);
    };
  };

  const stopPlaying = () => {
    source.stop();
    setIsLoading(false);
  };

  const speakThis = (text) => {
    setIsPlaying(true);
    setIsLoading(true);
    const url = new URL('http://localhost:8000/text-to-speech');
    url.searchParams.append('text_input', text);    

    fetch(url.toString())
      .then(response => response.blob())
      .then(blob => {        
        const fileReader = new FileReader();
        fileReader.onload = function () {
          const audioContext = new AudioContext();
          const arrayBuffer = this.result;
          audioContext.decodeAudioData(arrayBuffer, playAudio);
        };
        fileReader.readAsArrayBuffer(blob);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error in GET request:', error);
      });
  };

  return (
    <>
  <div className={'message' + (self ? ' message-self' : '')}>    
    <div className='message-text'>{text}</div>            
  </div>
  {!self ?
    (
      isPlaying ? 
      (
        isLoading ?
        <div className={'audio-field'}>      
        <div className='audio-text'>One moment...</div>
        </div>
        :
        <div className={'audio-field'}>    
        <button className='audio-play' onClick={() => stopPlaying()}>
          <img src={stop} width={20} height={20} alt="Stop button"/>
        </button>
        <div className='audio-text'>Stop the audio</div>
        </div>
      )
      :
      <div className={'audio-field'}>    
      <button className='audio-play' onClick={() => speakThis(text)}>
        <img src={play} width={20} height={20} alt="Play button"/>
      </button>
      <div className='audio-text'>Read this out loud</div>
      </div>
    )
    : null
  }
  </>
  );
};

const MessageWindow = ({ messages }) => {
  const messageWindow = React.useRef();

  return (
    <div className='message-window' ref={messageWindow}>
      {messages.map((msg, i) => (
        <Message key={i} text={msg.text} self={msg.self} />
      ))}
      <div>&nbsp;</div>
    </div>
  );
};

export default MessageWindow;
