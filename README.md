# RecallDesk 🧠

## Memory-Powered AI Customer Support Agent

RecallDesk is an AI-powered customer support agent that uses persistent memory to provide personalized support across multiple conversations.

Unlike a traditional chatbot that treats every conversation as new, RecallDesk can remember relevant information from a customer's previous interactions and use that context when helping them again.

---

## 🎯 Problem

Traditional AI customer-support systems often lose context between conversations.

A customer may explain their problem today, but when they return later, they may need to explain the same information again.

This creates a frustrating support experience and makes it difficult for AI agents to provide truly personalized assistance.

---

## 💡 Solution

RecallDesk gives every customer their own persistent memory.

The system:

1. Identifies the customer.
2. Retrieves relevant information from their previous conversations.
3. Sends the current problem and relevant history to the AI.
4. Generates a personalized support response.
5. Saves the new interaction for future conversations.

This allows RecallDesk to support **any customer and any type of support problem**.

---

## 🧠 Customer-Specific Memory

Each customer gets an isolated memory space.

For example:

```
Customer A
    ↓
recalldesk-customer-a

Customer B
    ↓
recalldesk-customer-b

Customer C
    ↓
recalldesk-customer-c
This keeps customer conversations separated and prevents information from one customer being mixed with another customer's history.

🏗️ Architecture
                    Customer
                       │
                       ▼
               ┌───────────────┐
               │  Streamlit UI │
               └───────┬───────┘
                       │
                       ▼
               ┌───────────────┐
               │  RecallDesk   │
               │     Agent     │
               └───────┬───────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
       ┌──────────────┐  ┌──────────────┐
       │  Hindsight   │  │     Groq     │
       │   Memory     │  │ GPT-OSS-20B  │
       └──────────────┘  └──────────────┘
              │                 │
              ▼                 ▼
       Customer History    AI Response
              │                 │
              └────────┬────────┘
                       ▼
              Personalized Support
✨ Key Features
🧠 Persistent customer memory
👤 Separate memory for every customer
💬 Natural-language customer support
🔄 Remembers previous interactions
🔐 Customer-specific memory isolation
🤖 AI-generated support responses
🌍 Supports any customer
🛠️ Supports any type of customer problem
⚡ Fast AI responses
🗄️ Long-term memory powered by Hindsight

🧪 Example
First conversation:
Customer: Sarah
Message:
My Python API keeps timing out.
RecallDesk provides troubleshooting assistance and stores the interaction in Sarah's memory.

Later conversation
Customer: Sarah
Message:
What do you remember about my previous issue?
RecallDesk retrieves relevant information from Sarah's previous interaction and uses it to provide a contextual response.

Different customer
Customer: Daniel
Message:
I cannot log into my account.
Daniel has a separate memory space from Sarah.
RecallDesk does not use Sarah's conversation when responding to Daniel.

🛠️ Technology Stack
Technology	Purpose
Python	Application logic
Streamlit	Web interface
Hindsight	Persistent customer memory
Groq	AI inference
GPT-OSS-20B	Response generation

📁 Project Structure
RecallDesk/
│
├── agent.py
├── ui.py
├── app.py
├── test_agent.py
├── test_groq.py
├── test_scenarios.py
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Run Locally
1. Clone the repository
git clone https://github.com/edunation07-cloud/RecallDesk.git
cd RecallDesk
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment
Windows PowerShell:
.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Configure API keys
Create a .env file in the project directory:
HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key
6. Start RecallDesk
streamlit run ui.py
The application will open in your browser.

🔐 Security
API keys are stored as environment variables and should not be committed to the GitHub repository.
The .env file is excluded using .gitignore.
For cloud deployment, API keys should be configured using the deployment platform's secret-management system.

🌐 Live Demo

Live Application:
Coming soon.

🎯 Hackathon Project
RecallDesk demonstrates how persistent memory can improve AI-powered customer support.
Instead of treating every interaction as a completely new conversation, RecallDesk maintains customer-specific context and uses relevant previous information to provide more personalized assistance.

🔮 Future Improvements
Possible future improvements includes:
🎫 Automatic support-ticket creation
👨‍💼 Human-agent handoff
📊 Customer support analytics
📝 Automatic conversation summaries
🔗 CRM integration
🌍 Multi-language support
🎙️ Voice-based customer support
😊 Customer sentiment detection
🏷️ Automatic issue categorization
🚀 Built With Python + Streamlit + Hindsight + Groq + GPT-OSS-20B

Built for a hackathon to demonstrate the power of persistent memory in AI customer support.
