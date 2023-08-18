import base64
from collections import OrderedDict
from dotenv import load_dotenv
import json
import os

import requests
import streamlit as st
from audiorecorder import audiorecorder

load_dotenv()

api_url = os.getenv("API_URL", "http://127.0.0.1:80")

# app title
st.title("Jarvis")

# app state
if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "messages" not in st.session_state:
    st.session_state.messages = []

mute_voice = {"None 🔇": None}


def format_voices(voices):
    """Format voices"""
    formatted_voices = []
    for name, desc in voices.items():
        if desc["description"] != "":
            name = f"{name}: {desc['description']}"
        if desc["use case"] != "":
            name = f"{name} ({desc['use case']})"
        formatted_voices.append((name, desc["id"]))
    return OrderedDict(formatted_voices)


# get default voices
if "voices" not in st.session_state:
    voices = format_voices(dict(requests.get(f"{api_url}/voices?custom=false").json()))
    voices.update(mute_voice)
    st.session_state.voices = voices

# get custom and default voices
if st.button("Get custom voices", disabled=st.session_state.disabled):
    with st.spinner("Getting available custom voices..."):
        voices = format_voices(dict(requests.get(f"{api_url}/voices").json()))
        voices.update(mute_voice)
        st.session_state.voices = voices

# parameters form
with st.form("app form"):
    input_type = st.radio(
        "Select input type",
        ("Audio", "Text"),
        disabled=st.session_state.disabled,
    )

    voice = st.selectbox(
        "Select output voice",
        st.session_state.voices.keys(),
        disabled=st.session_state.disabled,
    )

    submitted = st.form_submit_button(
        "Start",
        disabled=st.session_state.disabled,
    )
    if submitted:
        st.session_state.disabled = True
        st.experimental_rerun()

if st.session_state.disabled == False:
    st.stop()

# get audio prompt
audio = None
if input_type == "Audio":
    audio = audiorecorder("🔴 Click to speak", "🟥 Recording... Click to stop")

# get text prompt
text = None
if input_type == "Text":
    text = st.chat_input("Say something")

with st.spinner("Getting answer..."):
    answer = None
    # get answer from audio
    if audio is not None and len(audio) > 0:
        data = {"messages": json.dumps(st.session_state["messages"])}
        files = {"audio": audio.tobytes()}
        answer = requests.post(f"{api_url}/answer-audio", files=files, data=data).json()
    # get answer from text
    if text:
        data = {"text": text, "messages": st.session_state["messages"]}
        answer = requests.post(f"{api_url}/answer-text", json=data).json()
    if answer:
        st.session_state.messages += answer
        # print prompt and text answer
        for message in st.session_state.messages:
            msg = st.chat_message(message["role"])
            msg.write(message["content"])

        # get audio answer
        if st.session_state.voices[voice]:
            audio = requests.post(
                f"{api_url}/speak",
                json={
                    "text": answer[1]["content"],
                    "voice": st.session_state.voices[voice],
                },
            ).content

            # play audio answer
            audio_base64 = base64.b64encode(audio).decode("utf-8")
            audio_tag = (
                f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
            )
            st.markdown(audio_tag, unsafe_allow_html=True)
