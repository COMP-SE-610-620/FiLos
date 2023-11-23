import re
import numpy as np
import io
from TTS.utils.synthesizer import Synthesizer
from scipy.io.wavfile import write
from num2words import num2words

MODEL_PATH = "/root/.local/share/tts/tts_models--fi--css10--vits/model_file.pth.tar"
CONFIG_PATH = "/root/.local/share/tts/tts_models--fi--css10--vits/config.json"


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
        self.synthesizer = Synthesizer(MODEL_PATH, CONFIG_PATH, use_cuda=False)

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

        wav = self.synthesizer.tts(converted_text)

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
