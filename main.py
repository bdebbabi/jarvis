import os
import openai
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write

from elevenlabs import generate, stream

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

def speech2text():
    print("Listening")
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write('output.wav', fs, myrecording)  # Save as WAV file 

    audio_file= open('output.wav', "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)["text"]
    print(transcript)
    return transcript

def get_answer(messages):
    print("\nGetting answer")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Tu es un assistant un peu fou. Tu as beacoup d'humour. Tes réponses sont généralement courtes, seulement quelques phrases."},
        *messages
    ]
    )

    answer = completion.choices[0].message["content"]
    print(answer)
    return answer


def text2speech(text, voice="Me"):
    print("\nReading answer")
    voices = {
        "Me":"UROuXsTekbnk53kgBUFu",
        "Batman":"aKFzEXnRwz9b1NbZLVHP",
        "Macron": "fWHO0uNreUCMvhya5XOj"
    }
    audio = generate(
        api_key=elevenlabs_api_key,
        text=text,
        voice=voices[voice],
        model='eleven_multilingual_v1',
        stream=True
    )

    stream(audio)

if __name__=="__main__":
    user_input = 'y'
    messages = []
    while user_input == 'y':
        text = speech2text()
        messages.append({"role": "user", "content": text})
        answer = get_answer(messages)
        messages.append({"role": "assistant", "content": answer})
        text2speech(answer, "Me")
        print("\nType [y] to continue: ")
        user_input = input()
    