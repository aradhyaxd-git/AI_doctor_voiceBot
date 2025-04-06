import os
import platform
import subprocess
from gtts import gTTS
from elevenlabs import ElevenLabs, save
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def text_to_speech_with_fallback(input_text, output_filepath="final.mp3"):
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

    try:
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Brian",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        save(audio, output_filepath)
        print("✅ ElevenLabs used for speech synthesis.")

    except Exception as e:
        print("⚠️ ElevenLabs failed, falling back to gTTS.")
        print(f"Error: {e}")
        tts = gTTS(text=input_text, lang='en', slow=False)
        tts.save(output_filepath)
        print("✅ gTTS used instead.")
