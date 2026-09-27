
import streamlit as st
from hindsight_client import Hindsight

# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="RecallDesk AI",
    page_icon="💬",
    layout="wide"
)

st.title("💬 RecallDesk AI")
st.caption("AI Customer Support Chatbot with Long-Term Memory")

# ---------------- HINDSIGHT CONNECTION ----------------

@st.cache_resource
def get_hindsight_client():
    return Hindsight(
        base_url=st.secrets["HINDSIGHT_BASE_URL"],
        api_key=st.secrets["HINDSIGHT_API_KEY"],
    )


try:
    hindsight = get_hindsight_client()
    BANK_ID = st.secrets["HINDSIGHT_BANK_ID"]
except Exception as e:
    st.error(
        "Hindsight configuration is incomplete. "
        "Please check your Streamlit Secrets settings."
    )
    st.stop()

# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("🧠 RecallDesk Memory")
    st.write(
        "Customer details are stored in your Hindsight "
        "memory bank and can be recalled in future chats."
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Memory provider: Hindsight Cloud")

# ---------------- CHAT HISTORY ----------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------

prompt = st.chat_input(
    "Ask a question or share your order details..."
)

if prompt:
    # Display and store the user's message in the chat history.
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Remembering and preparing a response..."):
            try:
                # Store the user's message in Hindsight.
                hindsight.retain(
                    bank_id=BANK_ID,
                    content=f"Customer message: {prompt}",
                    context="RecallDesk AI customer support conversation",
                )

                # Generate a contextual answer using stored memories.
                response = hindsight.reflect(
                    bank_id=BANK_ID,
                    query=(
                        "You are RecallDesk AI, a helpful customer "
                        "support assistant. Answer the customer's "
                        "latest question using relevant stored memories. "
                        "If the information is not available, say so "
                        "and ask for the missing details. Do not invent "
                        "order numbers, customer details, or policies.\n\n"
                        f"Customer's latest message: {prompt}"
                    ),
                )

                answer = getattr(response, "text", None)

                if not answer:
                    answer = (
                        "I couldn't generate a response. "
                        "Please try asking in a different way."
                    )

            except Exception as e:
                answer = (
                    "⚠️ I couldn't connect to Hindsight or process "
                    "your request. Please check your API settings "
                    "and try again."
                )
                st.error(f"Connection or memory error: {e}")

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
)
