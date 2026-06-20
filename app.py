from utils.gemini_api import get_gemini_response
import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🤖 AI Assistant")

    mode = st.radio(
        "Choose Mode",
        [
            "Career Guidance",
            "Interview Preparation",
            "Learning Roadmap"
        ]
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main Page
# -----------------------------
st.title("🤖 AI Career & Interview Assistant")
st.caption("Your Personal AI Mentor")

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
prompt = st.chat_input("Ask your question...")

if prompt:

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # -----------------------------
    # Build Conversation History
    # -----------------------------
    conversation_history = ""

    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_history += f"{role}: {msg['content']}\n"

    # -----------------------------
    # Final Prompt for Gemini
    # -----------------------------
    final_prompt = f"""
You are an AI Career Assistant.

Current Mode: {mode}

Use the previous conversation for context.

Conversation:
{conversation_history}

Assistant:
"""

    # -----------------------------
    # Get Gemini Response
    # -----------------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_gemini_response(final_prompt)

        st.markdown(response)

    # Save Assistant Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )