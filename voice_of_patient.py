#step 1: setup audio recorder ((ffmpeg & portaudio))

#ffmpeg ,portaudio , pyaudio 
import logging
import speech_recognition as sr
from pydub import audio_segment
from io import BytesIO
from pydub import AudioSegment

AudioSegment.converter = r"C:\ffmpeg-7.1.1-full_build\bin\ffmpeg.exe"



logging.basicConfig(level=logging.INFO , format= '%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """Simplified function to record audio from microphone and save it as mp3 file

    Args: file_path(str): path to save the recorded audio file 
    timeout(int): maximum time to wait for phrase to start ( in seconds)
    phrase_time_limit (int): maximum time for phrase to be recorded (in seconds)
    """

    recognizer= sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise ...")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            logging.info("Start speaking now..")

            #record the audio
            audio_data = recognizer.listen(source, timeout=timeout , phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete")

            #convert the recorded audio to an mp3 file
            wav_data= audio_data.get_wav_data()
            audio_segment= AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")

            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error has occured: {e}")
audio_file_path="patient_voice_test.mp3"
record_audio(file_path=audio_file_path)

#step 2 : speech to text sst model for transcription 
import os 
from dotenv import load_dotenv

# Load environment variables from the .env file (if present)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
from groq import Groq

def transcribe_with_groq(GROQ_API_KEY, audio_file_path, stt_model="whisper-large-v3"): 
    try:
        client = Groq(api_key=GROQ_API_KEY)

        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text  # Extract text properly
    except Exception as e:
        print("Error in transcription:", str(e))
        return "Error: Could not transcribe audio."
