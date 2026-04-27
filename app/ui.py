import os
from typing import Optional, Tuple
import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

# ================= CONFIG =================
API_URL = os.getenv("ASSISTIQ_API_URL", "https://customer-support-agent-wppl.onrender.com/chat")

st.set_page_config(
    page_title="AssistIQ",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= STYLE =================
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: #F4F6FB;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#1E2A3A,#1A2432);
    color: #C8D8E8;
    border-right: 1px solid #2D3F55;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton button {
    width: 100%;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    color: #C8D8E8;
    text-align: left;
    padding: 10px;
    margin-bottom: 6px;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(37,99,235,0.3);
    color: white;
    transform: translateX(4px);
}

/* Chat bubbles */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background:#2563EB;
    color:white;
    margin-left:auto;
    max-width:70%;
    border-radius:16px 16px 4px 16px;
    padding:10px;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background:white;
    border:1px solid #E2E8F0;
    max-width:70%;
    border-radius:4px 16px 16px 16px;
    padding:10px;
}

/* Input */
[data-testid="stChatInput"] {
    border-radius:50px;
    border:1.5px solid #CBD5E0;
    background:white;
    box-shadow:0 8px 25px rgba(0,0,0,0.08);
    padding:6px;
}

</style>
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
    if st.button("💬 Recommend a Bluetooth speaker"):
        send_sample("Recommend a good Bluetooth speaker")
    if st.button("💬 Best laptop under ₹50,000"):
        send_sample("Best laptop under ₹50,000")

    st.divider()

    st.subheader("📦 Orders")
    if st.button("💬 Where is my order ORD001?"):
        send_sample("Where is my order ORD001?")

    st.divider()

    st.subheader("📜 Policies")
    if st.button("💬 What is the return policy?"):
        send_sample("What is your return policy?")

    st.divider()

    st.subheader("⚠️ Complaints")
    if st.button("💬 My product arrived damaged"):
        send_sample("My product arrived damaged")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ================= HEADER =================
st.markdown("""
<h2 style='text-align:center; font-family:serif; font-style:italic;'>
🛍️ AssistIQ — Customer Assistant
</h2>
<p style='text-align:center; color:#718096; font-size:13px; letter-spacing:1px;'>
SMART MULTI-AGENT AI · REAL-TIME SUPPORT
</p>
<hr>
""", unsafe_allow_html=True)


# ================= SESSION =================
if "messages" not in st.session_state:
    st.session_state.messages = []


# ================= HERO =================
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align:center; padding:60px 20px;">
        
        <div style="
            width:70px;
            height:70px;
            border-radius:18px;
            background:linear-gradient(135deg,#1E3A5F,#2563EB);
            display:flex;
            align-items:center;
            justify-content:center;
            margin:auto;
            font-size:28px;
            color:white;
            box-shadow:0 10px 25px rgba(37,99,235,0.3);
        ">
            🛍️
        </div>

        <h2 style="margin-top:20px;">How can I help you today?</h2>

        <p style="color:#718096; font-size:15px;">
            Order tracking, product recommendations, store policies, and complaint resolution.
        </p>

        <div style="margin-top:20px;">
            <span style="background:#EBF4FF;color:#2B6CB0;padding:8px 16px;border-radius:30px;margin:6px;display:inline-block;">
                🛍️ Products
            </span>
            <span style="background:#F0FFF4;color:#276749;padding:8px 16px;border-radius:30px;margin:6px;display:inline-block;">
                📦 Orders
            </span>
            <span style="background:#FFFAF0;color:#975A16;padding:8px 16px;border-radius:30px;margin:6px;display:inline-block;">
                📜 Policies
            </span>
            <span style="background:#FFF5F5;color:#9B2C2C;padding:8px 16px;border-radius:30px;margin:6px;display:inline-block;">
                ⚠️ Complaints
            </span>
        </div>

    </div>
    """, unsafe_allow_html=True)


# ================= CHAT =================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ================= INPUT =================
user_input = st.chat_input("Ask about orders, products or policies...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply, latency = call_chat_api(user_input)

        st.markdown(reply)

        if latency:
            st.caption(f"⏱ {latency:.2f}s")

    st.session_state.messages.append({"role": "assistant", "content": reply})
