from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import io

MODEL_PATH = "./models/facebook_mms_tts_fin/"

class TextToSpeechService:
    """
    Service for converting text to speech using the Vits model.

    Attributes:
        model (VitsModel): Pre-trained Vits model for text-to-speech.
        tokenizer (AutoTokenizer): Tokenizer for the Vits model.
    """

    def __init__(self):
        """
        Initialize the TextToSpeechService with pre-trained models.
        """
        self.model = VitsModel.from_pretrained(MODEL_PATH)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

    def text_to_speech(self, text: str) -> io.BytesIO:
        """
        Convert text to speech.

        Args:
            text (str): Input text to convert to speech.

        Returns:
            io.BytesIO: In-memory buffer containing the audio data.
        """
        inputs = self.tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            output = self.model(**inputs).waveform

        sampling_rate = self.model.config.sampling_rate

        # Create an in-memory buffer to hold the audio data
        buffer = io.BytesIO()
        scipy.io.wavfile.write(buffer, rate=sampling_rate, data=output.cpu().float().numpy().T)

        return buffer
# import torch
# from transformers import VitsModel, AutoTokenizer
# import io
# import numpy as np
# import soundfile as sf  # You can use soundfile for audio I/O

# MODEL_PATH = "./models/facebook_mms_tts_fin/"

# class TextToSpeechService:
#     def __init__(self):
#         self.model = VitsModel.from_pretrained(MODEL_PATH)
#         self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

#     def text_to_speech(self, text: str) -> io.BytesIO:
#         inputs = self.tokenizer(text, return_tensors="pt")

#         with torch.no_grad():
#             output = self.model(**inputs).waveform

#         sampling_rate = self.model.config.sampling_rate

#         # Create an in-memory buffer to hold the audio data
#         buffer = io.BytesIO()
        
#         # Convert audio data to bytes and write to the buffer
#         audio_bytes = output.cpu().float().numpy().tobytes()
#         buffer.write(audio_bytes)

#         return buffer
