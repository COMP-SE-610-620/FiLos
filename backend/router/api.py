from fastapi import APIRouter, File, WebSocket, UploadFile, Form, Response
import librosa
import librosa.display
import os
import torch
from fastapi.responses import JSONResponse

from services import (
    SpeechRecognitionService,
    APISpeechRecognition,
    TextToSpeechService,
    TextGenerationService,
)

router = APIRouter()

# Instantiate the TextGenerationService
text_generation_service = TextGenerationService()
asr_service = SpeechRecognitionService()  # Instantiate the service once
api_service = APISpeechRecognition()  # Instantiate the service once
use_inference_api = True

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@router.get("/")
def hello():
    return "FinGPT"


@router.post("/chat/text")
async def process_text_input(text_input: str = Form(...)):
    # Get response from TextGenerationService for text input
    response = text_generation_service.answer_question(text_input)
    return {"question": text_input, "response": response}


@router.post("/chat/speech")
async def transcribe_audio_endpoint(audio: UploadFile = File(...)):
    try:
        # Save the uploaded audio file temporarily
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as temp_audio:
            temp_audio.write(audio.file.read())
        # Transcribe the audio using the selected service
        if use_inference_api:
            converted_text = api_service.transcribe_audio_api(temp_audio_path)
        else:
            # Read the audio file using librosa
            audio_data, sample_rate = librosa.load(temp_audio_path, sr=None)
            audio_tensor = torch.tensor(audio_data)
            converted_text = asr_service.transcribe_audio(audio_tensor)

        converted_text_lower = converted_text.lower()
        return JSONResponse(content={'response': converted_text_lower}, status_code=200)

    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)

    finally:
        # Clean up: remove the temporary audio file
        os.remove(temp_audio_path)

@router.get("/text-to-speech/")
async def text_to_speech(text_input: str):
    tts_service = TextToSpeechService()
    finnish_text = finnish_number_to_text(text_input)
    audio_data = tts_service.text_to_speech(finnish_text)
    return Response(content=audio_data.getvalue(), media_type="audio/wav")


def finnish_number_to_text(input_str):
    def convert_number_to_text(number):
        if number == 0:
            return 'nolla'

        finnish_numbers = {
            1: 'yksi',
            2: 'kaksi',
            3: 'kolme',
            4: 'neljä',
            5: 'viisi',
            6: 'kuusi',
            7: 'seitsemän',
            8: 'kahdeksan',
            9: 'yhdeksän',
            10: 'kymmenen',
            11: 'yksitoista',
            12: 'kaksitoista',
            13: 'kolmetoista',
            14: 'neljätoista',
            15: 'viisitoista',
            16: 'kuusitoista',
            17: 'seitsemäntoista',
            18: 'kahdeksantoista',
            19: 'yhdeksäntoista',
            20: 'kaksikymmentä',
            30: 'kolmekymmentä',
            40: 'neljäkymmentä',
            50: 'viisikymmentä',
            60: 'kuusikymmentä',
            70: 'seitsemänkymmentä',
            80: 'kahdeksankymmentä',
            90: 'yhdeksänkymmentä',
            100: 'sata',
            200: 'kaksisataa',
            300: 'kolmesataa',
            400: 'neljäsataa',
            500: 'viisisataa',
            600: 'kuusisataa',
            700: 'seitsemänsataa',
            800: 'kahdeksansataa',
            900: 'yhdeksänsataa',
            1000: 'tuhat'
        }

        if 1 <= number <= 1000:
            result = []
            for base in sorted(finnish_numbers.keys(), reverse=True):
                count = number // base
                if count:
                    result.append(finnish_numbers[base])
                    number %= base

            return ' '.join(result) if result else 'nolla'
        else:
            return 'Number out of range (1-1000)'

    words = []
    parts = input_str.split()
    for part in parts:
        if ',' in part:
            # Handle decimal numbers with comma (,)
            int_part, decimal_part = part.split(',')
            try:
                int_text = convert_number_to_text(int(int_part))
                decimal_text = convert_number_to_text(int(decimal_part))
                words.append(f"{int_text} ja {decimal_text}")
            except ValueError:
                words.append(part)  # Handle cases where conversion to int fails
        elif '.' in part:
            # Handle decimal numbers with dot (.)
            int_part, decimal_part = part.split('.')
            try:
                int_text = convert_number_to_text(int(int_part))
                decimal_text = convert_number_to_text(int(decimal_part))
                words.append(f"{int_text} ja {decimal_text}")
            except ValueError:
                words.append(part)  # Handle cases where conversion to int fails
        elif part.isdigit():
            # Handle integer numbers
            words.append(convert_number_to_text(int(part)))
        else:
            words.append(part)

    return ' '.join(words)