import streamlit as st

from agent import respond, make_bank_id


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RecallDesk",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .brand {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -1px;
    }

    .tagline {
        font-size: 1.05rem;
        opacity: 0.65;
        margin-top: -5px;
        margin-bottom: 1.5rem;
    }

    .start-space {
        height: 45px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(130, 130, 130, 0.15);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "customer_id" not in st.session_state:
    st.session_state.customer_id = ""

if "customer_input" not in st.session_state:
    st.session_state.customer_input = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_message" not in st.session_state:
    st.session_state.pending_message = None


# =========================================================
# CUSTOMER CHANGE
# =========================================================

def switch_customer():
    new_customer = (
        st.session_state.customer_input
        .strip()
        .lower()
    )

    if new_customer != st.session_state.customer_id:
        st.session_state.customer_id = new_customer
        st.session_state.messages = []
        st.session_state.pending_message = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🧠 RecallDesk")

    st.caption("Memory-powered customer support")

    st.divider()

    st.markdown("### 👤 Customer")

    st.text_input(
        "Customer ID",
        placeholder="e.g. rahul",
        key="customer_input",
        on_change=switch_customer
    )

    if st.button(
        "🔗 Connect Customer",
        use_container_width=True
    ):

        new_customer = (
            st.session_state.customer_input
            .strip()
            .lower()
        )

        if new_customer:

            if new_customer != st.session_state.customer_id:
                st.session_state.messages = []
                st.session_state.pending_message = None

            st.session_state.customer_id = new_customer

        st.rerun()


    if st.session_state.customer_id:

        st.success(
            f"Customer connected: "
            f"{st.session_state.customer_id}"
        )


    st.divider()

    st.markdown("### 🔌 System Status")

    st.success("🧠 Hindsight Memory\n\nPersistent memory connected")

    st.success("🤖 Groq AI\n\nResponse engine connected")


    st.divider()

    st.markdown("### ⚡ How it works")

    st.caption("1. Customer sends a message")
    st.caption("2. RecallDesk searches their history")
    st.caption("3. Groq generates a response")
    st.caption("4. The interaction is remembered")


    st.divider()

    if st.button(
        "🗑️ Start New Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.pending_message = None

        st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="brand">🧠 RecallDesk</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="tagline">'
    'Customer support that remembers what matters.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# NO CUSTOMER CONNECTED
# =========================================================

if not st.session_state.customer_id:

    st.markdown("## Welcome to RecallDesk")

    st.write(
        "A memory-powered AI support agent that gives customers "
        "personalized help by remembering relevant conversation history."
    )

    st.divider()

    st.markdown("### Why RecallDesk?")


    # -----------------------------------------------------
    # FEATURE CARDS
    # -----------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(border=True):

            st.markdown("### 🧠 Persistent Memory")

            st.write(
                "Important customer context can be remembered "
                "across conversations."
            )


    with col2:

        with st.container(border=True):

            st.markdown("### 👤 Customer-Specific")

            st.write(
                "Each customer has their own memory space, "
                "keeping conversations separated."
            )


    with col3:

        with st.container(border=True):

            st.markdown("### 🤖 AI-Powered Support")

            st.write(
                "Groq generates contextual responses based "
                "on the current conversation and relevant history."
            )


    # -----------------------------------------------------
    # START MESSAGE
    # -----------------------------------------------------

    st.markdown(
        '<div class="start-space"></div>',
        unsafe_allow_html=True
    )

    st.info(
        "👉 Enter a Customer ID in the sidebar to start."
    )

    st.stop()


# =========================================================
# CUSTOMER MEMORY STATUS
# =========================================================

bank_id = make_bank_id(
    st.session_state.customer_id
)

st.info(
    f"🧠 Memory active — RecallDesk is maintaining "
    f"relevant history for **{st.session_state.customer_id}**."
)


# =========================================================
# SUGGESTED QUESTIONS
# =========================================================

if not st.session_state.messages:

    st.markdown("### Try asking")

    suggestions = [
        "What do you remember about me?",
        "I need help with my account.",
        "My API is having problems.",
        "What did we discuss previously?"
    ]

    cols = st.columns(4)

    for index, suggestion in enumerate(suggestions):

        with cols[index]:

            if st.button(
                suggestion,
                use_container_width=True
            ):

                st.session_state.pending_message = suggestion

                st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# HANDLE SUGGESTED QUESTION
# =========================================================

if st.session_state.pending_message:

    message = st.session_state.pending_message

    st.session_state.pending_message = None


    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    with st.chat_message("user"):

        st.markdown(message)


    # AI response
    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Recalling customer history..."
        ):

            try:

                answer = respond(
                    st.session_state.customer_id,
                    message
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                st.error(
                    f"RecallDesk encountered an error: {error}"
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "I'm sorry, but I couldn't process "
                            "that request right now."
                        )
                    }
                )


# =========================================================
# CHAT INPUT
# =========================================================

customer_message = st.chat_input(
    "Ask RecallDesk about your support issue..."
)


if customer_message:

    # -----------------------------------------------------
    # USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": customer_message
        }
    )

    with st.chat_message("user"):

        st.markdown(customer_message)


    # -----------------------------------------------------
    # AI RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🧠 Recalling customer history..."
        ):

            try:

                answer = respond(
                    st.session_state.customer_id,
                    customer_message
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as error:

                st.error(
                    f"RecallDesk encountered an error: {error}"
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "I'm sorry, but I couldn't process "
                            "that request right now."
                        )
                    }
                )