import React, { useState } from 'react';
import './MessageWindow.css';
import play from "./play.png";
import stop from "./stop.png";
let source;

const Message = ({ text, self }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [cachedBlobUrl, setBlobUrl] = useState(null);

  const stopPlaying = () => {
    source.pause();
    source.currentTime = 0;
    setIsPlaying(false);
    setIsLoading(false);
  };

  const speakThis = (text) => {
    setIsPlaying(true);
    setIsLoading(true);
    const url = new URL('http://localhost:8000/text-to-speech');
    url.searchParams.append('text_input', text);

    // Check if the file is already in the cache
    if (cachedBlobUrl) {
      playAudio(cachedBlobUrl);
      setIsLoading(false);
      return;
    }

    fetch(url.toString())
      .then(response => response.blob())
      .then(blob => {
        const blobUrl = URL.createObjectURL(blob);

        // Store the Blob URL in the cache variable
        setBlobUrl(blobUrl);

        playAudio(blobUrl);
        setIsLoading(false);
      })
      .catch(error => {
        console.error('Error in GET request:', error);
        setIsLoading(false);
      });
  };

  // Function to play audio from Blob URL
  const playAudio = (blobUrl) => {
    source = new Audio(blobUrl);
    source.play().then(() => {
      setIsPlaying(true);
    });
    source.addEventListener('ended', onAudioEnded);
  };

  const onAudioEnded = () => {
    setIsPlaying(false);
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
                    <img src={stop} width={20} height={20} alt="Stop button" />
                  </button>
                  <div className='audio-text'>Stop the audio</div>
                </div>
            )
            :
            <div className={'audio-field'}>
              <button className='audio-play' onClick={() => speakThis(text)}>
                <img src={play} width={20} height={20} alt="Play button" />
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
