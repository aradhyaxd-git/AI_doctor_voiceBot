# 🩺 AI Doctor VoiceBot

An AI-powered medical assistant that understands your voice and provides diagnosis using Generative AI. Built with **Streamlit** for the frontend, **GROQ Cloud (LLaMA Vision 3B)** for LLM inference, and tools like `gTTS` and `PyAudio` for audio interaction.

---

## ⚙️ Features

✅ **Voice-based Diagnosis**  
→ Speak your symptoms. The bot captures your voice, converts it to text, and sends it to a cloud-based LLM.  
→ The response is displayed in text and also spoken using `gTTS`.

✅ **Text + Voice Response**  
→ Get medical advice in readable and audible formats.

✅ **Interactive UI**  
→ Simple and clean interface powered by Streamlit.

---

## 🧠 Tech Stack

| Layer           | Tools / Technologies                           |
|----------------|-------------------------------------------------|
| Frontend        | `Streamlit`                                     |
| AI Model        | `GROQ Cloud` - LLaMA Vision 3B                  |
| Voice Input     | `PyAudio`, `SpeechRecognition`, `wave`         |
| Voice Output    | `gTTS` - Google Text-to-Speech                  |
| Backend         | `Python`                                        |

---

## 🚀 How It Works

1. **Record Voice**  
   → Your voice input is recorded and converted to text.

2. **Generate Prompt**  
   → This text is formatted as a prompt for LLaMA Vision 3B (hosted on GROQ Cloud).

3. **Receive Response**  
   → The AI's response is shown in text.  
   → Then it's spoken out loud using `gTTS`.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ai-doctor-voicebot.git
cd ai-doctor-voicebot
pip install -r requirements.txt
streamlit run app.py
