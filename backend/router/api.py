from fastapi import APIRouter, File, WebSocket, UploadFile, Form, Response
import soundfile as sf
import io
from services import SpeechRecognitionService, TextToSpeechService, TextGenerationService

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint to accept and send text messages.

    Args:
        websocket (WebSocket): WebSocket instance.

    Returns:
        None
    """
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")

@router.get("/")
def hello():
    """
    Default route to say hello.

    Returns:
        str: A greeting message.
    """
    return "FinGPT"

@router.post("/chat")
async def process_input(
    file: UploadFile = File(None),
    text_input: str = Form(None),
):
    """
    Process input, which can be either audio or text, and generate a response.

    Args:
        file (UploadFile): Optional audio file (speech input).
        text_input (str): Optional text input.

    Returns:
        dict: Response containing the generated text.
    """
    if file and file.content_type.startswith('audio/'):
        # Handle audio file input (speech)
        audio_data = sf.read(io.BytesIO(await file.read()))[0]
        asr_service = SpeechRecognitionService()
        converted_text = asr_service.transcribe_audio(audio_data)
        # text_generation_service = TextGenerationService()
        # response = text_generation_service.generate_text(converted_text)
        response = converted_text
        return {"response": response}

    elif text_input:
        # Handle text input
        # text_generation_service = TextGenerationService()
        # response = text_generation_service.generate_text(text_input)
        response = text_input
        return {"response": response}

    else:
        return {"error": "Invalid input. Provide either an audio file or text."}

@router.get("/text-to-speech/")
async def text_to_speech(text_input: str):
    """
    Convert text to speech and return the audio data.

    Args:
        text_input (str): Text to convert to speech.

    Returns:
        Response: Audio data as a response with media type "audio/wav".
    """
    tts_service = TextToSpeechService()
    audio_data = tts_service.text_to_speech(text_input)
    return Response(content=audio_data.getvalue(), media_type="audio/wav")
