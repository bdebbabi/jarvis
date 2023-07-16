import os
import openai
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write

from elevenlabs import generate, stream

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")


def record_audio():
    print("Listening")
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write("output.wav", fs, myrecording)  # Save as WAV file


def speech2text():
    audio_file = open("output.wav", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]
    print(transcript)
    return transcript


def get_answer(messages):
    print("\nGetting answer")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant un peu fou. Tu as beacoup d'humour. Tes réponses sont généralement courtes, seulement quelques phrases.",
            },
            *messages,
        ],
    )

    answer = completion.choices[0].message["content"]
    print(answer)
    return answer


def text2speech(text, voice):
    print("\nReading answer")
    audio = generate(
        api_key=elevenlabs_api_key,
        text=text,
        voice=voice,
        model="eleven_multilingual_v1",
        stream=True,
    )

    return audio


if __name__ == "__main__":
    user_input = "y"
    messages = []
    while user_input == "y":
        record_audio()
        text = speech2text()
        messages.append({"role": "user", "content": text})
        answer = get_answer(messages)
        messages.append({"role": "assistant", "content": answer})
        text2speech(answer, "Arnold")
        print("\nType [y] to continue: ")
        user_input = input()
