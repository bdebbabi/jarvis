from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import StreamingResponse
import json

from jarvis import speech2text, get_answer, text2speech

from pydantic import BaseModel


class Answer(BaseModel):
    text: str
    voice: str


app = FastAPI()


@app.post("/answer/")
async def answer(messages: str = Form(), audio: UploadFile = File(...)):
    wav_file = open("output.wav", "wb")
    wav_file.write(audio.file.read())
    text = speech2text()
    messages = json.loads(messages)

    messages.append({"role": "user", "content": text})
    answer = get_answer(messages)
    messages.append({"role": "assistant", "content": answer})

    return messages[-2:]


@app.post("/speak/")
async def speak(answer: Answer):
    audio = text2speech(answer.text, answer.voice)

    # Set the appropriate headers for the response
    headers = {
        "Content-Disposition": "attachment; filename=audio.wav",
        "Content-Type": "audio/wav",
    }

    # Return a streaming response with the audio data
    return StreamingResponse(audio, media_type="audio/wav", headers=headers)
