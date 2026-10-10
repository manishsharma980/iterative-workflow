import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv('my_api_key')

client = genai.Client(api_key=api_key)

for model in client.models.list():
    if "generateContent" in model.supported_actions:
        print(model.name)