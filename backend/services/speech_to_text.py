from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import requests
from pydub import AudioSegment
from pydub.playback import play
import librosa

LANG_ID = "fi"
MODEL_ID = "Finnish-NLP/wav2vec2-large-uralic-voxpopuli-v2-finnish"

class LocalSpeechRecognition:
    @staticmethod
    def transcribe_audio(audio_file_path: str) -> str:

        # Replace 'your_audio_file.wav' with the path to your audio file.
        AUDIO_FILE_PATH = audio_file_path

        processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
        model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)

        # Load the audio file
        speech_array, sampling_rate = librosa.load(AUDIO_FILE_PATH, sr=16_000)

        # Preprocess the input
        inputs = processor(speech_array, sampling_rate=16_000, return_tensors="pt", padding=True)

        with torch.no_grad():
            logits = model(inputs.input_values, attention_mask=inputs.attention_mask).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentence = processor.batch_decode(predicted_ids)[0]

        print("Predicted Sentence:", predicted_sentence)
        return predicted_sentence