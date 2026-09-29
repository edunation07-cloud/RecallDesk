import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY was not found.")
    raise SystemExit

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Say hello to the RecallDesk hackathon team in one short sentence."
        }
    ]
)

print("\nGroq response:")
print(response.choices[0].message.content)

print("\nSUCCESS! Groq is working.")