import os
import streamlit as st
import sounddevice as sd  # type: ignore
import numpy as np
import scipy.io.wavfile as wav
from brain_of_doctor import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_doctor import text_to_speech_with_fallback
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# System prompt
system_prompt = """You have to act as a professional doctor, ik you are not but please act so.
What is in the image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them.
Do not add any number or special characters in your response.
Your response should be in one long paragraph or in points.
Also, always answer as if you are talking to a real person.
Do not say 'In this image I see', but say 'With what I see, I think you have ...'
Do not respond as an AI model in markdown; your answer should mimic an actual professional doctor, not an AI bot.
Keep your answers concise. No preamble; start your answers right away, please."""

# UI
st.title("🩺 AI Doctor With Vision & Voice")

# Voice recording
st.header("🎙 Record Your Voice")

# Session states
if "recording" not in st.session_state:
    st.session_state.recording = False
if "sample_rate" not in st.session_state:
    st.session_state.sample_rate = 44100
if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

# Start recording
if not st.session_state.recording:
    if st.button("🎤 Start Recording"):
        st.session_state.recording = True
        st.write("🔴 Recording... Speak now!")

        duration = 60  # 60 sec max
        st.session_state.audio_buffer = sd.rec(
            int(duration * st.session_state.sample_rate),
            samplerate=st.session_state.sample_rate,
            channels=1,
            dtype=np.int16
        )
        sd.wait()

# Stop recording
if st.session_state.recording:
    if st.button("⏹ Stop Recording"):
        st.session_state.recording = False
        st.write("✅ Recording stopped!")

        # Save file
        st.session_state.audio_path = "recorded_audio.wav"
        wav.write(st.session_state.audio_path, st.session_state.sample_rate, st.session_state.audio_buffer)

        st.audio(st.session_state.audio_path, format="audio/wav")
        st.success("Recording saved!")

# Upload image
st.header("🖼 Upload a Medical Image")
image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Analyze button
if st.button("⚡ Analyze"):
    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        # Convert voice to text
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY, st.session_state.audio_path, stt_model="whisper-large-v3"
        )
        st.text_area("🗣 Speech to Text:", speech_to_text_output)

        # Analyze image if available
        if image_file:
            image_path = "uploaded_image." + image_file.name.split('.')[-1]
            with open(image_path, "wb") as f:
                f.write(image_file.read())

            doctor_response = analyze_image_with_query(
                query=system_prompt + " " + speech_to_text_output,
                encoded_image=encode_image(image_path),
                model="llama-3.2-11b-vision-preview"
            )
        else:
            doctor_response = "No image provided for me to analyze."

        st.text_area("👨‍⚕️ Doctor's Response:", doctor_response)

        # Text to speech with fallback
        with st.spinner("🔊 Converting to voice..."):
            text_to_speech_with_fallback(doctor_response, "final.mp3")

        # Play audio
        st.markdown(
        """
        <audio src="final.mp3" autoplay>
        </audio>
        """,
        unsafe_allow_html=True
)


    else:
        st.warning("⚠️ Please record your voice before analyzing.")
