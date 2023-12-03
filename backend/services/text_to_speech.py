import re
import numpy as np
import io
import os
from TTS.utils.synthesizer import Synthesizer
from scipy.io.wavfile import write
from num2words import num2words
import torch
from TTS.api import TTS


def convert_numbers_to_text(text, lang="fi"):
    """
    Convert numbers from text to text format.
    """
    number_pattern = re.compile(r"\d+,\d+|\d+")

    def replace_with_words(match):
        number_str = match.group(0)
        if "," in number_str:
            whole, decimal = number_str.split(",")
            return (
                num2words(int(whole), lang=lang)
                + " pilkku "
                + num2words(int(decimal), lang=lang)
            )
        else:
            return num2words(int(number_str), lang=lang)

    return number_pattern.sub(replace_with_words, text)

class TextToSpeechService:
    """
    Service for converting text to speech using the Mozilla TTS model.
    """

    def __init__(self):
        """
        Initialize the TextToSpeechService with the specified Mozilla TTS model.
        """
        # Get device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(model_name="tts_models/fi/css10/vits", progress_bar=False).to(device)

    def text_to_speech(self, text: str) -> io.BytesIO:
        """
        Convert text to speech.

        Args:
            text (str): Input text to convert to speech.

        Returns:
            io.BytesIO: In-memory buffer containing the audio data.
        """
        # Convert numbers in the text to words
        converted_text = convert_numbers_to_text(text)

        wav = self.tts.tts(converted_text, speaker_wav="audio.wav")

        # Convert to 16-bit PCM
        wav = np.int16(wav / np.max(np.abs(wav)) * 32767)
        sampling_rate = (
            22050  # Typical sampling rate for Mozilla TTS, adjust as necessary
        )

        # Create an in-memory buffer to hold the audio data
        buffer = io.BytesIO()
        write(buffer, rate=sampling_rate, data=wav)
        buffer.seek(0)  # Reset buffer to the beginning

        return buffer