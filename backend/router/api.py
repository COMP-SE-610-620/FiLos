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


@router.post("/chat")
async def process_input(
    file: UploadFile = File(None),
    text_input: str = Form(None),
):
    if file and file.content_type.startswith("audio/"):
        # Handle audio file input (speech)
        audio_data = sf.read(io.BytesIO(await file.read()))[0]
        asr_service = SpeechRecognitionService()
        converted_text = asr_service.transcribe_audio(audio_data)

        # Get response from TextGenerationService
        response = text_generation_service.answer_question([converted_text])
        return {"response": response}

    elif text_input:
        # Handle text input

        # Get response from TextGenerationService
        response = text_generation_service.answer_question([text_input])
        return {"response": response}

    else:
        return {"error": "Invalid input. Provide either an audio file or text."}


@router.get("/text-to-speech/")
async def text_to_speech(text_input: str):
    tts_service = TextToSpeechService()
    audio_data = tts_service.text_to_speech(text_input)
    return Response(content=audio_data.getvalue(), media_type="audio/wav")