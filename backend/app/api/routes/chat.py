# app/api/chat.py
import os
import requests
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from app.models import VoiceChatResponse, ChatResponse, ChatRequest
from langchain_openai import ChatOpenAI

router = APIRouter(prefix="/chat", tags=["chats"])

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "your_voice_id")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

openai_llm = ChatOpenAI(
    model=OPENAI_MODEL_NAME,
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=OPENAI_API_KEY,
)

def generate_openai_response(system_prompt: str, user_message: str) -> str:

    messages = [
        (
            "system",
            system_prompt
        ),
        (
            "user",
            user_message
        ),
    ]

    return openai_llm.invoke(messages).content

def check_user_response() -> str:

    system_prompt = Prompt.Chat_detect_prompt


@router.post("/get_text_response", response_model=ChatResponse)
async def chat_with_openai(request: ChatRequest) -> ChatResponse:
    """
    Endpoint to generate a response using OpenAI gpt-4o model
    """
    history = request.history
    system_prompt = """
        You are learning language assistant. 
        History: {history}
    """
    user_input = request.message

    ai_response = generate_openai_response(system_prompt, user_input)
    print("AI result: ", ai_response)
    message = ai_response

    return ChatResponse(message=message)

def elevenlabs_stt(audio_bytes: bytes) -> str:
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "application/json"
    }
    files = {
        "file": ("audio.wav", audio_bytes, "audio/wav"),
        "model_id": (None, "scribe_v1"),
    }
    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    return response.json()["text"]

def elevenlabs_tts(text: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "audio/mpeg",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.content

@router.post("/voicechat")
async def voice_chat(file: UploadFile = File(...)):
    # 1. Get text from ElevenLabs STT
    audio_bytes = await file.read()
    try:
        user_text = elevenlabs_stt(audio_bytes)
        print("Elevenlabs STT result: ", user_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"STT failed: {e}")

    # 2. Get AI response from OpenAI
    system_prompt = "You are a language learning assistant. only generate response as 2 sentences in English, not over 3 sentences. max letters are 500"
    ai_response = openai_llm.invoke([
        ("system", system_prompt),
        ("user", user_text)
    ]).content

    print("AI response: ", ai_response)

    # # 3. Get TTS from ElevenLabs
    # try:
    #     audio_response = elevenlabs_tts(ai_response)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"TTS failed: {e}")

    # 4. Return audio as streaming response (or as base64 if you prefer)
    return ai_response

@router.post("/voicechat/textstream")
async def stream_text(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    try:
        user_text = elevenlabs_stt(audio_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"STT failed: {e}")

    system_prompt = "You are a language learning assistant. Only generate response as 2 sentences in English, not over 3 sentences. Max letters are 500."

    async def event_generator():
        full_text = ""
        for chunk in openai_llm.stream([("system", system_prompt), ("user", user_text)]):
            full_text += chunk.content
            yield {"data": chunk.content}
            await asyncio.sleep(0)
        # After streaming text, send a special event with the full text
        yield {"event": "done", "data": full_text}

    return EventSourceResponse(event_generator())