
import streamlit as st
import re

st.set_page_config(
    page_title="RecallDesk AI",
    page_icon="🧠",
    layout="wide"
)

# Demo memory stored only in the current session
if "messages" not in st.session_state:
    st.session_state.messages = []

if "memories" not in st.session_state:
    st.session_state.memories = {}


st.title("🧠 RecallDesk AI")
st.caption(
    "Customer support assistant with memory — interactive demo prototype"
)


with st.sidebar:
    st.subheader("Memory status")
    st.warning(
        "Demo memory active · Hindsight Cloud is not connected."
    )
    st.caption("Memories last only during this app session.")

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
    low = message.lower().strip()
    memories = st.session_state.memories

    # Save customer name
    name_match = re.search(
        r"\bmy name is\s+([A-Za-z][A-Za-z '-]{0,30})",
        message,
        re.I
    )

    if name_match:
        name = name_match.group(1).strip().rstrip(".!,")
        memories["name"] = name

    # Save support preference
    pref_match = re.search(
        r"\bi prefer\s+(email|phone|telephone|chat|text|whatsapp)\b",
        message,
        re.I
    )

    if pref_match:
        pref = pref_match.group(1).lower()
        memories["support preference"] = (
            "phone" if pref == "telephone" else pref
        )

    # Save order reference
    order_match = re.search(
        r"\border\s*(?:number|reference|#)?\s*(?:is\s*)?"
        r"([A-Z0-9-]{4,})\b",
        message,
        re.I
    )

    if order_match:
        memories["order reference"] = order_match.group(1)

    # Answer questions about the order
    if any(q in low for q in [
        "what is my order number",
        "what is my order reference",
        "show my order",
        "what is my order"
    ]):
        if "order reference" in memories:
            return (
                f"Your order reference is "
                f"{memories['order reference']}."
            )
        return (
            "I don't have your order reference saved yet. "
            "Tell me: My order number is RD123."
        )

    # Answer questions about the customer's name
    if any(q in low for q in [
        "what is my name",
        "who am i",
        "remember my name"
    ]):
        if "name" in memories:
            return f"Your name is {memories['name']}."
        return (
            "I don't have your name saved yet. "
            "Tell me: My name is Maya."
        )

    # Answer questions about support preference
    if any(q in low for q in [
        "how do i prefer",
        "support preference",
        "how should you contact",
        "how do you contact"
    ]):
        if "support preference" in memories:
            return (
                f"You prefer support by "
                f"{memories['support preference']}."
            )
        return (
            "I don't have a support preference saved yet. "
            "Tell me: I prefer email support."
        )

    # Show all saved memories
    if any(q in low for q in [
        "what do you remember",
        "show my memory",
        "what have you saved"
    ]):
        if not memories:
            return (
                "I haven't saved any customer details yet. "
                "Share your name or support preference first."
            )

        saved = "; ".join(
            f"{key}: {value}" for key, value in memories.items()
        )
        return f"Here is what I have saved: {saved}."

    # Confirm saved details
    if name_match or pref_match or order_match:
        saved = ", ".join(
            f"{key}: {value}"
            for key, value in memories.items()
        )
        return f"Thanks! I saved this in demo memory: {saved}."

    # General delivery response
    if any(q in low for q in ["delivery", "deliver", "order"]):
        return (
            "I can help with your delivery. "
            "Please share your order reference, "
            "and I'll keep it in this demo session."
        )

    return (
        "I can help with order delivery and remember basic "
        "customer details in this demo. Try: "
        "'My name is Maya. I prefer email support.'"
    )


# Display previous messages
for item in st.session_state.messages:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])


# Chat input
prompt = st.chat_input("Type a customer message…")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = respond(prompt)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)


st.divider()
st.caption(
    "Prototype note: This build uses simple in-session demo memory. "
    "It does not connect to Hindsight Cloud or an external LLM."
            )
           
