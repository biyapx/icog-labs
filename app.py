import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Summarize the following data, considering this knowledge base: ____.  Then, provide a concise summary of the data: ____",
)
print(response.text)