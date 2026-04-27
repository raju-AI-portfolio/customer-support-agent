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

# ================= PROFESSIONAL STYLING =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global font */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* Page background */
[data-testid="stAppViewContainer"] {
    background: #F8FAFF !important;
}

/* Hide Streamlit menu and footer */
#MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #1C2B3A !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: #1C2B3A !important;
    padding-top: 1.5rem !important;
}

/* Sidebar title */
[data-testid="stSidebar"] h1 {
    color: #FFFFFF !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar subheaders */
[data-testid="stSidebar"] h3 {
    color: #7FA8C9 !important;
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-family: 'Inter', sans-serif !important;
    margin-top: 4px !important;
}

/* Sidebar caption */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #4A6A88 !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 10px 0 !important;
}

/* Sidebar buttons - WHITE text - target every possible child */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] .stButton > button:focus,
[data-testid="stSidebar"] .stButton > button:active {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
    text-align: left !important;
    padding: 10px 14px !important;
    margin-bottom: 5px !important;
    transition: all 0.15s !important;
    white-space: normal !important;
    height: auto !important;
    line-height: 1.5 !important;
}
/* Force WHITE on every inner element Streamlit creates */
[data-testid="stSidebar"] .stButton > button *,
[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button div,
[data-testid="stSidebar"] .stButton > button span,
[data-testid="stSidebar"] .stButton > button small,
[data-testid="stSidebar"] .stButton > button label {
    color: #FFFFFF !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    background: transparent !important;
}
[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] .stButton > button:hover * {
    background: rgba(37,99,235,0.3) !important;
    border-color: rgba(37,99,235,0.6) !important;
    color: #FFFFFF !important;
    transform: translateX(3px) !important;
}

/* Last button = Clear Chat (red) */
[data-testid="stSidebar"] .stButton:last-child > button {
    background: rgba(220,50,50,0.1) !important;
    border-color: rgba(220,50,50,0.25) !important;
    color: #F87171 !important;
}
[data-testid="stSidebar"] .stButton:last-child > button:hover {
    background: rgba(220,50,50,0.25) !important;
    color: #FFFFFF !important;
}

/* ── MAIN AREA ── */
[data-testid="stMain"] .block-container {
    padding: 2rem 2.5rem 5rem !important;
    max-width: 960px !important;
}

/* Page title */
[data-testid="stMain"] h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #0F1E2E !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em !important;
}

/* Page caption */
[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    color: #94A3B8 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* Divider */
[data-testid="stMain"] hr {
    border-color: #E2E8F0 !important;
    margin: 0.8rem 0 !important;
}

/* ── CHAT MESSAGES ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] {
    background: #2563EB !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    max-width: 78% !important;
    margin-left: auto !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] p {
    color: #FFFFFF !important;
    font-size: 0.93rem !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 4px 18px 18px 18px !important;
    padding: 12px 18px !important;
    max-width: 78% !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] p {
    color: #1A202C !important;
    font-size: 0.93rem !important;
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
    border-radius: 50px !important;
    border: 1.5px solid #CBD5E0 !important;
    background: #FFFFFF !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.07) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    color: #1A202C !important;
    padding: 12px 16px !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #A0AEC0 !important;
}

/* Send button SVG arrow - white */
[data-testid="stChatInput"] button {
    background: #2563EB !important;
    background-color: #2563EB !important;
    border-radius: 50% !important;
    border: none !important;
}
[data-testid="stChatInput"] button svg {
    filter: brightness(0) invert(1) !important;
}
[data-testid="stChatInput"] button svg path {
    fill: #FFFFFF !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 8px; }
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

    st.subheader("🛍️ PRODUCTS")
    if st.button("💬 Recommend a Bluetooth speaker"):
        send_sample("Recommend a good Bluetooth speaker")
    if st.button("💬 Best laptop under ₹50,000"):
        send_sample("Best laptop under ₹50,000")
    if st.button("💬 Noise-cancelling headphones"):
        send_sample("Suggest noise-cancelling headphones")
    if st.button("💬 Best mobile under ₹30,000"):
        send_sample("Best mobile phone under ₹30,000")

    st.divider()
    st.subheader("📦 ORDERS")
    if st.button("💬 Where is my order ORD001?"):
        send_sample("Where is my order ORD001?")
    if st.button("💬 Track my order ORD002"):
        send_sample("Track my order ORD002")
    if st.button("💬 Status of ORD003?"):
        send_sample("What is the status of ORD003?")
    if st.button("💬 Has ORD004 been delivered?"):
        send_sample("Has my order ORD004 been delivered?")

    st.divider()
    st.subheader("📜 POLICIES")
    if st.button("💬 What is the return policy?"):
        send_sample("What is your return policy?")
    if st.button("💬 How do I get a refund?"):
        send_sample("How do I get a refund?")
    if st.button("💬 Warranty policy"):
        send_sample("What is the warranty policy?")
    if st.button("💬 How long does shipping take?"):
        send_sample("How long does shipping take?")

    st.divider()
    st.subheader("⚠️ COMPLAINTS")
    if st.button("💬 My product arrived damaged"):
        send_sample("My product arrived damaged")
    if st.button("💬 I received the wrong item"):
        send_sample("I received the wrong item")
    if st.button("💬 My order has not arrived"):
        send_sample("My order has not arrived yet")
    if st.button("💬 Raise a complaint"):
        send_sample("I want to raise a complaint")

    st.divider()
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ================= MAIN =================
st.title("🛍️ AssistIQ — Customer Assistant")
st.caption("Smart Multi-Agent AI · Real-Time Support")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome card
if not st.session_state.messages:
    st.markdown("""
<div style="text-align:center;padding:3rem 1rem 2rem;">
    <div style="width:80px;height:80px;border-radius:22px;
                background:linear-gradient(135deg,#1E3A5F,#2563EB);
                display:flex;align-items:center;justify-content:center;
                font-size:2.2rem;margin:0 auto 20px;
                box-shadow:0 8px 24px rgba(37,99,235,0.25);">🛍️</div>
    <div style="font-size:1.8rem;font-weight:700;color:#0F1E2E;
                margin-bottom:12px;font-family:'Inter',sans-serif;
                letter-spacing:-0.02em;">
        How can I help you today?
    </div>
    <div style="font-size:0.92rem;color:#64748B;max-width:420px;
                margin:0 auto 12px;line-height:1.75;">
        Order tracking, product recommendations, store policies,
        and complaint resolution.
    </div>
    <div style="font-size:0.8rem;color:#94A3B8;margin-bottom:28px;">
        ← Pick a question from the sidebar or type below
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;justify-content:center;">
        <div style="background:#EBF4FF;border:1.5px solid #93C5FD;border-radius:50px;
                    padding:10px 20px;font-size:0.88rem;color:#1D4ED8;font-weight:600;">
            🛍️ Products</div>
        <div style="background:#F0FFF4;border:1.5px solid #6EE7B7;border-radius:50px;
                    padding:10px 20px;font-size:0.88rem;color:#065F46;font-weight:600;">
            📦 Orders</div>
        <div style="background:#FFFBEB;border:1.5px solid #FCD34D;border-radius:50px;
                    padding:10px 20px;font-size:0.88rem;color:#92400E;font-weight:600;">
            📜 Policies</div>
        <div style="background:#FFF1F2;border:1.5px solid #FDA4AF;border-radius:50px;
                    padding:10px 20px;font-size:0.88rem;color:#9F1239;font-weight:600;">
            ⚠️ Complaints</div>
    </div>
</div>
""", unsafe_allow_html=True)

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
        if latency:
            st.caption(f"⏱ {latency:.2f}s")
    st.session_state.messages.append({"role": "assistant", "content": reply})
