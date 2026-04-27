import os
from typing import Optional, Tuple
import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

API_URL = os.getenv("ASSISTIQ_API_URL", "https://customer-support-agent-wppl.onrender.com/chat")

# ✅ FORCE SIDEBAR ALWAYS OPEN
st.set_page_config(
    page_title="AssistIQ",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ SESSION FIX: ensure sidebar never stays collapsed
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# 🔥 HARD FIX: auto-expand sidebar if collapsed
st.markdown("""
<script>
(function() {
    function forceSidebar() {
        try {
            const doc = window.parent.document;
            const sidebar = doc.querySelector('[data-testid="stSidebar"]');
            const btn = doc.querySelector('[data-testid="collapsedControl"] button');

            if (sidebar && sidebar.getAttribute('aria-expanded') === 'false') {
                if (btn) btn.click();
            }
        } catch(e) {}
    }

    setTimeout(forceSidebar, 200);
    setTimeout(forceSidebar, 800);
    setTimeout(forceSidebar, 1500);
})();
</script>
""", unsafe_allow_html=True)

# ================= API =================
def call_chat_api(message: str) -> Tuple[str, Optional[float]]:
    try:
        resp = requests.post(API_URL, json={"message": message}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "⚠️ Empty response"), data.get("latency")
    except ConnectionError:
        return "⚠️ Cannot reach backend", None
    except Timeout:
        return "⚠️ Request timed out", None
    except requests.HTTPError as e:
        return f"⚠️ HTTP error {e.response.status_code}", None
    except Exception:
        return "⚠️ Unexpected error", None


def send_sample(q: str):
    st.session_state.messages.append({"role": "user", "content": q})
    st.rerun()


# ================= SIDEBAR =================
with st.sidebar:
    st.title("🛍️ AssistIQ")
    st.caption("Customer Support Platform")

    st.divider()

    st.subheader("🛍️ Products")
    if st.button("Bluetooth speaker"):
        send_sample("Recommend a good Bluetooth speaker")
    if st.button("Laptop under 50k"):
        send_sample("Best laptop under ₹50,000")

    st.divider()

    st.subheader("📦 Orders")
    if st.button("Track ORD001"):
        send_sample("Where is my order ORD001?")

    st.divider()

    st.subheader("📜 Policies")
    if st.button("Return policy"):
        send_sample("What is your return policy?")

    st.divider()

    st.subheader("⚠️ Complaints")
    if st.button("Damaged product"):
        send_sample("My product arrived damaged")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ================= MAIN =================
st.title("🛍️ AssistIQ — Customer Assistant")
st.caption("AI Customer Support")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input
user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, latency = call_chat_api(user_input)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
