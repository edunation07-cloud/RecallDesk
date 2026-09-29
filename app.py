import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

# -----------------------------
# API KEYS
# -----------------------------

hindsight_key = os.getenv("HINDSIGHT_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

if not hindsight_key:
    print("ERROR: HINDSIGHT_API_KEY was not found.")
    raise SystemExit

if not groq_key:
    print("ERROR: GROQ_API_KEY was not found.")
    raise SystemExit


# -----------------------------
# CLIENTS
# -----------------------------

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=hindsight_key
)

groq = Groq(api_key=groq_key)

bank_id = "recalldesk-demo"


# -----------------------------
# CUSTOMER MESSAGE
# -----------------------------

customer_message = input("\nCustomer: ")


# -----------------------------
# RECALL CUSTOMER MEMORY
# -----------------------------

memory_result = hindsight.recall(
    bank_id=bank_id,
    query=customer_message
)

memories = []

for memory in memory_result.results:
    memories.append(memory.text)

memory_context = "\n".join(memories)

if not memory_context:
    memory_context = "No previous customer information found."


# -----------------------------
# GENERATE SUPPORT RESPONSE
# -----------------------------

prompt = f"""
You are RecallDesk, an AI customer support agent.

Use the customer's previous information when it is relevant.

Previous customer memory:
{memory_context}

Current customer message:
{customer_message}

Respond naturally and helpfully.
Do not mention that you are reading a memory database.
"""


response = groq.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

answer = response.choices[0].message.content


# -----------------------------
# SAVE NEW INTERACTION
# -----------------------------

hindsight.retain(
    bank_id=bank_id,
    content=f"Customer said: {customer_message}\nSupport agent responded: {answer}"
)


# -----------------------------
# DISPLAY
# -----------------------------

print("\nRecallDesk:")
print(answer)

print("\nMemory updated successfully.")

hindsight.close()