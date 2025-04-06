#Step 1 : Setup GROQ api Key 
import os 
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#Step 2: Convert image to required format
import base64 #ye jo bhi data hai usko string mei convert kardeta hai

#image_path= "acne.jpg"
def encode_image(image_path):
    image_file= open(image_path,"rb")
    return base64.b64encode(image_file.read()).decode('utf-8')

#Step 3: Setup multi modal LLM
from groq import Groq

query="Is there something wrong with my face?"
model="llama-3.2-90b-vision-preview"
def analyze_image_with_query(query,model,encoded_image):
    client= Groq(api_key=GROQ_API_KEY)
    messages=[
        {
            "role":"user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url":{
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
         }]
    chat_completion=client.chat.completions.create(
    messages=messages,
    model=model 
    ) 
    return chat_completion.choices[0].message.content 