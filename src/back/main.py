from collections import OrderedDict
import json

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from back.jarvis import (
    get_answer,
    speech2text,
    text2speech,
    get_voices as get_11labs_voices,
)


app = FastAPI()


@app.post("/answer-audio/")
async def answer_audio(
    messages: str = Form(), audio: UploadFile = File(...)
) -> list[dict]:
    """Returns answer from audio input and the conversation so far

    Args:
        messages (str, optional): the conversation so far. Defaults to Form().
        audio (UploadFile, optional): audio input. Defaults to File(...).

    Returns:
        list[dict]: text answer
    """
    wav_file = open("output.wav", "wb")
    wav_file.write(audio.file.read())
    text = speech2text()
    messages = json.loads(messages)

    messages.append({"role": "user", "content": text})
    answer = get_answer(messages)
    messages.append({"role": "assistant", "content": answer})

    return messages[-2:]


class Prompt(BaseModel):
    messages: list
    text: str


@app.post("/answer-text/")
async def answer_text(prompt: Prompt) -> list[dict]:
    """Returns answer from text input and the conversation so far

    Args:
        prompt (Prompt): Contains text input and the conversation so far

    Returns:
        list[dict]: text answer
    """
    messages = prompt.messages

    messages.append({"role": "user", "content": prompt.text})
    answer = get_answer(messages)
    messages.append({"role": "assistant", "content": answer})

    return messages[-2:]


class Answer(BaseModel):
    text: str
    voice: str


@app.post("/speak/")
async def speak(answer: Answer) -> StreamingResponse:
    """Converts text answer to audio

    Args:
        answer (Answer): Contains text to convert and voice id to use

    Returns:
        StreamingResponse: audio response
    """
    audio = text2speech(answer.text, answer.voice)

    # Set the appropriate headers for the response
    headers = {
        "Content-Disposition": "attachment; filename=audio.wav",
        "Content-Type": "audio/wav",
    }

    # Return a streaming response with the audio data
    return StreamingResponse(audio, media_type="audio/wav", headers=headers)


@app.get("/voices/")
async def get_voices(custom: bool = True) -> OrderedDict:
    """Returns available elevenlabs voices

    Args:
        custom (bool): whether to return custom voices or only the default ones.

    Returns:
        OrderedDict: available voices
    """
    return get_11labs_voices(custom)
