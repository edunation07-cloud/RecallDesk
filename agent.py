import os
import re
import asyncio

from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not HINDSIGHT_API_KEY:
    raise RuntimeError("HINDSIGHT_API_KEY was not found in .env")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY was not found in .env")


# ============================================================
# CLIENTS
# ============================================================

groq = Groq(api_key=GROQ_API_KEY)


HINDSIGHT_BASE_URL = "https://api.hindsight.vectorize.io"


# ============================================================
# CUSTOMER MEMORY BANK
# ============================================================

def make_bank_id(customer_id):
    """
    Convert any customer name/ID into a safe Hindsight bank ID.

    Examples:

        Rahul
        -> recalldesk-rahul

        John Smith
        -> recalldesk-john-smith

        customer_123
        -> recalldesk-customer_123

        ACME-1001
        -> recalldesk-acme-1001
    """

    if not customer_id:
        raise ValueError("Customer ID cannot be empty.")

    customer_id = str(customer_id).strip().lower()

    # Replace spaces and unsupported characters.
    customer_id = re.sub(
        r"[^a-z0-9_-]+",
        "-",
        customer_id
    )

    # Remove duplicate hyphens.
    customer_id = re.sub(
        r"-+",
        "-",
        customer_id
    )

    # Remove leading/trailing hyphens.
    customer_id = customer_id.strip("-")

    if not customer_id:
        raise ValueError("Customer ID must contain letters or numbers.")

    return f"recalldesk-{customer_id}"


# ============================================================
# HINDSIGHT ASYNC HELPERS
# ============================================================

async def _hindsight_create_bank(client, bank_id, customer_id):
    """
    Create/update a customer's memory bank.
    """

    return await client.acreate_bank(
        bank_id=bank_id,
        name=f"RecallDesk - {customer_id}"
    )


async def _hindsight_recall(client, bank_id, query):
    """
    Retrieve memories relevant to the customer's message.
    """

    return await client.arecall(
        bank_id=bank_id,
        query=query,
        max_tokens=4096,
        budget="mid"
    )


async def _hindsight_retain(client, bank_id, content):
    """
    Save the latest interaction to the customer's memory.
    """

    return await client.aretain(
        bank_id=bank_id,
        content=content
    )


def _run_hindsight_async(async_function):
    """
    Run one Hindsight async operation inside its own event loop.

    This keeps Hindsight's aiohttp networking away from
    Streamlit's execution context.
    """

    async def runner():
        client = Hindsight(
            base_url=HINDSIGHT_BASE_URL,
            api_key=HINDSIGHT_API_KEY
        )

        try:
            return await async_function(client)

        finally:
            await client.aclose()

    return asyncio.run(runner())


# ============================================================
# CREATE / ENSURE CUSTOMER
# ============================================================

def ensure_customer(customer_id):
    """
    Make sure this customer's memory bank exists.

    This works for ANY customer.
    """

    bank_id = make_bank_id(customer_id)

    _run_hindsight_async(
        lambda client: _hindsight_create_bank(
            client,
            bank_id,
            customer_id
        )
    )

    return bank_id


# ============================================================
# MEMORY RETRIEVAL
# ============================================================

def get_customer_memories(bank_id, customer_message):
    """
    Retrieve information from this customer's previous
    conversations.

    For normal questions:
        Search for memories related to the current problem.

    For broad memory questions:
        Search for important information from the customer's
        previous interactions.
    """

    message_lower = customer_message.lower()

    broad_memory_questions = [
        "what do you remember",
        "what do you know about me",
        "what do you know about my history",
        "what do you remember about me",
        "tell me about my history",
        "previous conversations",
        "previous issues",
        "my history",
        "our previous conversation",
        "our previous conversations",
        "what happened before",
        "do you remember me"
    ]

    if any(
        phrase in message_lower
        for phrase in broad_memory_questions
    ):

        recall_query = """
Find important information from this customer's
previous support interactions.

Return relevant information about:

- previous problems
- previous technical issues
- previous support requests
- products or services discussed
- technologies or frameworks mentioned
- customer preferences
- account-related information
- previous troubleshooting steps
- unresolved issues
- important facts the customer previously shared

Only return information actually present in this customer's
memory.
"""

    else:

        recall_query = customer_message

    result = _run_hindsight_async(
        lambda client: _hindsight_recall(
            client,
            bank_id,
            recall_query
        )
    )

    memories = []

    if hasattr(result, "results"):

        for memory in result.results:

            if hasattr(memory, "text"):
                memories.append(memory.text)

            elif isinstance(memory, dict):
                text = memory.get("text")

                if text:
                    memories.append(text)

    if not memories:
        return "No relevant previous customer information was found."

    return "\n".join(memories)


# ============================================================
# GROQ RESPONSE GENERATION
# ============================================================

def generate_response(
    customer_id,
    customer_message,
    memory_context
):
    """
    Generate a customer-support response.

    This is intentionally generic and can handle
    any type of customer problem.
    """

    prompt = f"""
You are RecallDesk, a professional AI customer-support agent.

You are helping customer:

{customer_id}

Your job is to understand the customer's current problem
and provide a useful, clear, accurate support response.

IMPORTANT RULES:

1. Help with ANY customer-support problem.
2. Do not assume the problem belongs to a predefined category.
3. Use previous customer information only when relevant.
4. Never invent customer history.
5. Never invent account details.
6. Never claim an action was completed if you cannot actually
   perform that action.
7. If information is missing, ask a clear follow-up question
   when necessary.
8. Give practical troubleshooting steps when appropriate.
9. Do not mention Hindsight.
10. Do not mention memory databases.
11. Do not mention prompts or internal systems.
12. Do not expose internal implementation details.
13. Keep the response focused on the customer's issue.
14. If the customer asks what you remember, summarize the
    relevant previous information provided in the memory section.
15. If no relevant previous information exists, say so naturally.
16. Treat the current customer message as the main priority.
17. Never confuse this customer with another customer.
18. Be professional, friendly, and concise.

CUSTOMER'S PREVIOUS RELEVANT INFORMATION:

{memory_context}

CURRENT CUSTOMER MESSAGE:

{customer_message}

Now respond directly to the customer.
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

    return response.choices[0].message.content


# ============================================================
# SAVE INTERACTION
# ============================================================

def save_interaction(
    bank_id,
    customer_message,
    response
):
    """
    Store the customer's latest conversation in their
    own Hindsight memory bank.
    """

    content = f"""
Customer message:
{customer_message}

RecallDesk response:
{response}
"""

    _run_hindsight_async(
        lambda client: _hindsight_retain(
            client,
            bank_id,
            content
        )
    )


# ============================================================
# MAIN RECALLDESK PIPELINE
# ============================================================

def respond(customer_id, customer_message):
    """
    Complete RecallDesk pipeline.

    Works with ANY customer and ANY support problem.

        Customer
            ↓
        Customer-specific memory bank
            ↓
        Retrieve relevant history
            ↓
        Groq AI
            ↓
        Personalized response
            ↓
        Save interaction
    """

    if not customer_id or not str(customer_id).strip():
        raise ValueError("Please provide a customer ID.")

    if not customer_message or not str(customer_message).strip():
        raise ValueError("Please provide a customer message.")

    customer_id = str(customer_id).strip()
    customer_message = str(customer_message).strip()

    # --------------------------------------------------------
    # 1. Create/get this customer's memory bank
    # --------------------------------------------------------

    bank_id = ensure_customer(customer_id)

    # --------------------------------------------------------
    # 2. Retrieve this customer's relevant history
    # --------------------------------------------------------

    memory_context = get_customer_memories(
        bank_id,
        customer_message
    )

    # --------------------------------------------------------
    # 3. Generate AI support response
    # --------------------------------------------------------

    response = generate_response(
        customer_id,
        customer_message,
        memory_context
    )

    # --------------------------------------------------------
    # 4. Save this interaction
    # --------------------------------------------------------

    save_interaction(
        bank_id,
        customer_message,
        response
    )

    return response


# ============================================================
# CLEANUP
# ============================================================

def close_clients():
    """
    Kept for compatibility with the rest of the project.

    Hindsight clients are created and closed per operation,
    so there is no persistent Hindsight client to close here.
    """

    pass