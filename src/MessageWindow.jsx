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

    const fetchAndCacheAudio = async () => {
      try {
        const cache = await caches.open('audio-cache');
        const response = await cache.match(url.toString());

        if (response) {
          const audioBuffer = await response.arrayBuffer();
          const audioContext = new AudioContext();
        } else {
          const fetchResponse = await fetch(url.toString());
          const blob = await fetchResponse.blob();

          const cacheResponse = new Response(blob);
          await cache.put(url.toString(), cacheResponse);

          const arrayBuffer = await blob.arrayBuffer();
          const audioContext = new AudioContext();
          audioContext.decodeAudioData(arrayBuffer, playAudio);
        }

        setIsLoading(false);
      } catch (error) {
        console.error('Error in GET request', error);
      }
  };

  return new Promise((resolve) => {
    fetchAndCacheAudio().then(() => {
      resolve();
    });
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
