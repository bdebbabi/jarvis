import streamlit as st
from audiorecorder import audiorecorder
import requests
import base64
import json
from jarvis import *

api_url = "http://127.0.0.1:8000"
voices = {
    "Me": "UROuXsTekbnk53kgBUFu",
    "Batman": "aKFzEXnRwz9b1NbZLVHP",
    "Macron": "fWHO0uNreUCMvhya5XOj",
}

# app title
st.title("Jarvis")

# app state
if "disabled" not in st.session_state:
    st.session_state.disabled = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# voices form
with st.form("app form"):
    voice = st.selectbox(
        "Select a voice",
        voices.keys(),
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
audio = audiorecorder("🔴 Click to speak", "🟥 Recording... Click to stop")
with st.spinner("Getting answer..."):
    if len(audio) > 0:
        # get text answer
        files = {"audio": audio.tobytes()}
        data = {"messages": json.dumps(st.session_state["messages"])}
        answer = requests.post(f"{api_url}/answer", files=files, data=data).json()

        # print prompt and text answer
        st.session_state.messages += answer
        for message in st.session_state.messages:
            msg = st.chat_message(message["role"])
            msg.write(message["content"])

        # get audio answer
        audio = requests.post(
            f"{api_url}/speak",
            json={"text": answer[1]["content"], "voice": voices[voice]},
        ).content

        # play audio answer
        audio_base64 = base64.b64encode(audio).decode("utf-8")
        audio_tag = (
            f'<audio autoplay="true" src="data:audio/wav;base64,{audio_base64}">'
        )
        st.markdown(audio_tag, unsafe_allow_html=True)
