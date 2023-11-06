from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch

MODEL_PATH = "jonatasgrosman/wav2vec2-large-xlsr-53-finnish"

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
