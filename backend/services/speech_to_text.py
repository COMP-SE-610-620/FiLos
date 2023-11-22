from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import requests
from pydub import AudioSegment
from pydub.playback import play

MODEL_PATH = "jonatasgrosman/wav2vec2-large-xlsr-53-finnish"
##private
API_URL = "https://api-inference.huggingface.co/models/jonatasgrosman/wav2vec2-large-xlsr-53-finnish"
HEADERS = {"Authorization": "Bearer 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"}

class SpeechRecognitionService:
    """
    Service for transcribing audio data using the Wav2Vec2 model.

    Attributes:
        processor (Wav2Vec2Processor): Processor for the Wav2Vec2 model.
        model (Wav2Vec2ForCTC): Pre-trained Wav2Vec2 model for audio transcription.
    """

    def __init__(self):
        """
        Initialize the SpeechRecognitionService with pre-trained models.
        """
        self.processor = Wav2Vec2Processor.from_pretrained(MODEL_PATH)
        self.model = Wav2Vec2ForCTC.from_pretrained(MODEL_PATH)

    def transcribe_audio(self, audio_data: torch.Tensor) -> str:
        """
        Transcribe audio data into text.

        Args:
            audio_data (torch.Tensor): Audio data as a PyTorch tensor.

        Returns:
            str: Transcribed text from the audio data.
        """
        audio_tensor = audio_data
        input_features = self.processor(audio_tensor, return_tensors="pt")

        with torch.no_grad():
            output = self.model(**input_features)

        predicted_ids = torch.argmax(output.logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids)

        return transcription[0]

class APISpeechRecognition:
    @staticmethod
    def transcribe_audio_api(audio_file_path: str) -> str:
        flac_filename = "converted_audio.flac"
        APISpeechRecognition.convert_to_flac(audio_file_path, flac_filename)

        with open(flac_filename, "rb") as f:
            data = f.read()

        response = requests.post(API_URL, headers=HEADERS, data=data)
        result = response.json()

        return result.get("text", "")

    @staticmethod
    def convert_to_flac(input_file, output_file):
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format="flac")