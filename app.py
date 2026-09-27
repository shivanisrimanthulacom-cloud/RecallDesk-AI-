import streamlit as st
from datetime import datetime

st.set_page_config(page_title="RecallDesk AI", page_icon="🧠", layout="wide")

# Demo-mode memory is kept in this browser session only. It is not Hindsight persistence.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "memories" not in st.session_state:
    st.session_state.memories = {}

st.title("🧠 RecallDesk AI")
st.caption("Customer support assistant with memory — interactive demo prototype")

with st.sidebar:
    st.subheader("Memory status")
    st.warning("Demo memory active · Hindsight Cloud is not connected in this starter.")
    st.caption("Demo memories last only while this app session is active.")
    if st.button("Clear chat and demo memory", use_container_width=True):
        st.session_state.messages = []
        st.session_state.memories = {}
        st.rerun()
    st.divider()
    st.subheader("Customer memory")
    if st.session_state.memories:
        for key, value in st.session_state.memories.items():
            st.markdown(f"**{key.title()}**")
            st.write(value)
    else:
        st.info("No customer details saved yet.")

def respond(message: str) -> str:
    low = message.lower()
    # Simple demo extraction for a name and support preference
    import re
    name_match = re.search(r"\bmy name is\s+([A-Za-z][A-Za-z '-]{0,40})", message, re.I)
    if name_match:
        name = name_match.group(1).strip().rstrip(".!,")
        st.session_state.memories["name"] = name
    pref_match = re.search(r"\bi prefer\s+(email|phone|telephone|chat|text|whatsapp)\b", message, re.I)
    if pref_match:
        pref = pref_match.group(1).lower()
        st.session_state.memories["support preference"] = "phone" if pref == "telephone" else pref

    order_match = re.search(r"\border\s*(?:number|#)?\s*([A-Z0-9-]{4,})", message, re.I)
    if order_match:
        st.session_state.memories["order reference"] = order_match.group(1)

    if any(q in low for q in ["what is my name", "who am i", "remember my name"]):
        return f"Your name is {st.session_state.memories['name']}." if "name" in st.session_state.memories else "I don't have your name saved yet. Tell me: “My name is Maya.”"
    if any(q in low for q in ["how do i prefer", "support preference", "how should you contact", "how do you contact"]):
        return f"You prefer support by {st.session_state.memories['support preference']}." if "support preference" in st.session_state.memories else "I don't have a support preference saved yet. Tell me, for example: “I prefer email support.”"
    if any(q in low for q in ["what do you remember", "show my memory", "what have you saved"]):
        if not st.session_state.memories:
            return "I haven't saved any customer details yet. Share your name or support preference first."
        return "Here is what I have saved: " + "; ".join(f"{k}: {v}" for k, v in st.session_state.memories.items()) + "."
    if "delivery" in low or "deliver" in low or "order" in low:
        return "I can help with your delivery. Please share your order reference, and I’ll keep it in this demo session."
    if name_match or pref_match:
        saved = []
        if "name" in st.session_state.memories: saved.append(f"name: {st.session_state.memories['name']}")
        if "support preference" in st.session_state.memories: saved.append(f"preferred support: {st.session_state.memories['support preference']}")
        return "Thanks — I saved " + " and ".join(saved) + " in the demo memory for this session."
    return "I can help with order delivery and remember basic customer details in this demo. Try: “My name is Maya. I prefer email support.”"

for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])

prompt = st.chat_input("Type a customer message…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    answer = respond(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

st.divider()
st.caption("Prototype note: This build uses simple in-session demo memory. It does not call Hindsight Cloud or an external LLM.")
