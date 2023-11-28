from fastapi import APIRouter, File, WebSocket, UploadFile, Form, Response
import librosa
import librosa.display
import os
import torch
from fastapi.responses import JSONResponse
from num2words import num2words


from services import (
    LocalSpeechRecognition,
    TextToSpeechService,
    TextGenerationService,
)

router = APIRouter()


text_generation_service = TextGenerationService()
local_asr_service = LocalSpeechRecognition()
tts_service = TextToSpeechService()


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
        converted_text = local_asr_service.transcribe_audio(temp_audio_path)
        return JSONResponse(content={"response": converted_text}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    finally:
        # Clean up: remove the temporary audio file
        os.remove(temp_audio_path)


@router.get("/text-to-speech/")
async def text_to_speech(text_input: str):
    audio_data = tts_service.text_to_speech(text_input)
    return Response(content=audio_data.getvalue(), media_type="audio/wav")
