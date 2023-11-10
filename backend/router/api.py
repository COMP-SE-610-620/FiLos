from fastapi import APIRouter, File, WebSocket, UploadFile, Form, Response
import soundfile as sf
import io
from services import (
    SpeechRecognitionService,
    TextToSpeechService,
    TextGenerationService,
)

router = APIRouter()

# Instantiate the TextGenerationService
text_generation_service = TextGenerationService()


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
async def process_speech_input(file: UploadFile = File(...)):
    if file.content_type.startswith("audio/"):
        # Handle audio file input (speech)
        audio_data = sf.read(io.BytesIO(await file.read()))[0]
        asr_service = SpeechRecognitionService()
        converted_text = asr_service.transcribe_audio(audio_data)
        
        # Get response from TextGenerationService
        response = text_generation_service.answer_question(converted_text)
        return {"question": converted_text, "response": response}
    else:
        return {"error": "Invalid input. Provide an audio file with the 'audio/' content type."}

@router.get("/text-to-speech/")
async def text_to_speech(text_input: str):
    tts_service = TextToSpeechService()
    audio_data = tts_service.text_to_speech(text_input)
    return Response(content=audio_data.getvalue(), media_type="audio/wav")