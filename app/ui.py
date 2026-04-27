import os
from typing import Optional, Tuple
import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

API_URL = os.getenv("ASSISTIQ_API_URL", "https://customer-support-agent-wppl.onrender.com/chat")

st.set_page_config(
    page_title="AssistIQ",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,500&display=swap');

/* ── GLOBAL ── */
html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'Inter', sans-serif !important;
    background: #F4F6FB !important;
}

/* ── HIDE CHROME (keep sidebar toggle) ── */
#MainMenu, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], footer {
    visibility: hidden !important;
    display: none !important;
}

/* ── SIDEBAR TOGGLE — big blue button ── */
[data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    width: 36px !important;
    height: 36px !important;
    background: #2563EB !important;
    border-radius: 50% !important;
    top: 50% !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.4) !important;
    cursor: pointer !important;
    z-index: 999 !important;
}
[data-testid="collapsedControl"] svg {
    width: 20px !important;
    height: 20px !important;
    filter: brightness(0) invert(1) !important;
}

/* ── MAIN CONTENT ── */
[data-testid="stMain"] .block-container {
    padding: 2rem 2.5rem 6rem !important;
    max-width: 980px !important;
}

/* ── PAGE TITLE ── */
[data-testid="stMain"] h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.2rem !important;
    font-weight: 600 !important;
    color: #1A202C !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stMain"] hr {
    border: none !important;
    border-top: 1px solid #E2E8F0 !important;
    margin: 1rem 0 !important;
}

[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    font-size: 0.75rem !important;
    color: #A0AEC0 !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-style: normal !important;
}

/* ═══════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background-color: #1E2A3A !important;
    border-right: 2px solid #2D3F55 !important;
    min-width: 260px !important;
    max-width: 270px !important;
}

[data-testid="stSidebar"] > div:first-child {
    background-color: #1E2A3A !important;
    padding-top: 1.4rem !important;
}

/* Sidebar ALL text nodes */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small {
    color: #C8D8E8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    line-height: 1.6 !important;
}

[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #5A7A9A !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 10.5px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    margin: 0 0 8px 0 !important;
    padding: 0 !important;
    background: transparent !important;
}

[data-testid="stSidebar"] h2:first-of-type {
    font-family: 'Playfair Display', serif !important;
    font-size: 20px !important;
    font-style: italic !important;
    text-transform: none !important;
    letter-spacing: -0.01em !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    margin-bottom: 2px !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #5A7A9A !important;
    font-size: 10px !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    font-style: normal !important;
}

[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.1) !important;
    margin: 12px 0 !important;
}

/* ═══════════════════════════════════════
   SIDEBAR BUTTONS — override Streamlit red
═══════════════════════════════════════ */
[data-testid="stSidebar"] .stButton > button,
[data-testid="stSidebar"] [data-testid="stButton"] > button,
[data-testid="stSidebar"] button[kind="secondary"],
[data-testid="stSidebar"] button {
    width: 100% !important;
    background-color: rgba(255,255,255,0.07) !important;
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
    color: #C8D8E8 !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 8px 12px !important;
    margin-bottom: 5px !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
    line-height: 1.5 !important;
    white-space: normal !important;
    height: auto !important;
    min-height: unset !important;
    box-shadow: none !important;
}

/* Every child of sidebar button */
[data-testid="stSidebar"] .stButton > button *,
[data-testid="stSidebar"] [data-testid="stButton"] > button *,
[data-testid="stSidebar"] button[kind="secondary"] *,
[data-testid="stSidebar"] button * {
    color: #C8D8E8 !important;
    font-size: 12.5px !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    background: transparent !important;
}

[data-testid="stSidebar"] .stButton > button:hover,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover,
[data-testid="stSidebar"] button:hover {
    background-color: rgba(37,99,235,0.25) !important;
    background: rgba(37,99,235,0.25) !important;
    border-color: rgba(37,99,235,0.5) !important;
    color: #FFFFFF !important;
    transform: translateX(3px) !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stButton > button:hover *,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover *,
[data-testid="stSidebar"] button:hover * {
    color: #FFFFFF !important;
    background: transparent !important;
}

/* Clear Chat button — last button red tint */
[data-testid="stSidebar"] .stButton:last-child > button,
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button {
    background-color: rgba(239,68,68,0.12) !important;
    background: rgba(239,68,68,0.12) !important;
    border-color: rgba(239,68,68,0.3) !important;
    color: #FC8181 !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] .stButton:last-child > button *,
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button * {
    color: #FC8181 !important;
    background: transparent !important;
}

[data-testid="stSidebar"] .stButton:last-child > button:hover,
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button:hover {
    background-color: rgba(239,68,68,0.25) !important;
    background: rgba(239,68,68,0.25) !important;
    color: #FFFFFF !important;
}

/* ═══════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════ */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 4px 0 !important;
}

[data-testid="stChatMessage"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.94rem !important;
    line-height: 1.78 !important;
    margin: 0 !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] {
    background: #2563EB !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.25) !important;
    max-width: 78% !important;
    margin-left: auto !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 4px 18px 18px 18px !important;
    padding: 12px 18px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    max-width: 78% !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] p { color: #1A202C !important; }

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stCaptionContainer"] p {
    font-size: 0.72rem !important;
    color: #A0AEC0 !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    font-style: normal !important;
}

/* ═══════════════════════════════════════
   CHAT INPUT + SEND BUTTON
═══════════════════════════════════════ */
[data-testid="stChatInput"] {
    border-radius: 50px !important;
    border: 1.5px solid #CBD5E0 !important;
    background: #FFFFFF !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
    padding: 4px 6px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15), 0 4px 16px rgba(0,0,0,0.08) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    color: #1A202C !important;
    padding: 12px 16px !important;
    line-height: 1.6 !important;
    background: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #A0AEC0 !important;
}

/* Send button — BLUE with WHITE arrow */
[data-testid="stChatInput"] button,
[data-testid="stChatInput"] button:focus,
[data-testid="stChatInput"] button:active,
[data-testid="stChatInput"] button[kind="primary"],
[data-testid="stChatInput"] button[kind="secondary"] {
    background-color: #2563EB !important;
    background: #2563EB !important;
    border-radius: 50% !important;
    border: none !important;
    outline: none !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.4) !important;
    min-width: 40px !important;
    min-height: 40px !important;
    width: 40px !important;
    height: 40px !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.15s !important;
    color: #FFFFFF !important;
}
[data-testid="stChatInput"] button:hover {
    background-color: #1D4ED8 !important;
    background: #1D4ED8 !important;
    transform: scale(1.08) !important;
    box-shadow: 0 6px 18px rgba(37,99,235,0.5) !important;
}
/* White arrow — filter is the nuclear option */
[data-testid="stChatInput"] button svg,
[data-testid="stChatInput"] button svg *,
[data-testid="stChatInput"] button svg path,
[data-testid="stChatInput"] button svg circle,
[data-testid="stChatInput"] button svg rect {
    fill: #FFFFFF !important;
    stroke: #FFFFFF !important;
    color: #FFFFFF !important;
    filter: brightness(0) invert(1) !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] p {
    font-size: 0.85rem !important;
    color: #718096 !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #CBD5E0; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ── API CALL ──────────────────────────────────────────────────────────────────
def call_chat_api(message: str) -> Tuple[str, Optional[float]]:
    try:
        resp = requests.post(API_URL, json={"message": message}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "⚠️ The server returned an empty response."), data.get("latency")
    except ConnectionError:
        return "⚠️ Cannot reach the server. Please check that the backend is running.", None
    except Timeout:
        return "⚠️ The request timed out. Please try again.", None
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        return f"⚠️ Server error (HTTP {status}). Please try again.", None
    except ValueError:
        return "⚠️ Received an unexpected response from the server.", None
    except RequestException as e:
        return f"⚠️ Network error: {e}", None


def send_sample(q: str):
    st.session_state.messages.append({"role": "user", "content": q})
    st.rerun()


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛍️ AssistIQ")
    st.caption("Customer Support Platform")
    st.markdown("---")

    st.markdown("**🛍️ PRODUCT RECOMMENDATIONS**")
    if st.button("💬 Recommend a Bluetooth speaker"):    send_sample("Recommend a good Bluetooth speaker")
    if st.button("💬 Best laptop under ₹50,000"):        send_sample("Best budget laptop under ₹50,000")
    if st.button("💬 Noise-cancelling headphones"):      send_sample("Suggest noise-cancelling headphones")
    if st.button("💬 Best mobile under ₹30,000"):        send_sample("Best mobile phone under ₹30,000")

    st.markdown("---")
    st.markdown("**📦 ORDER TRACKING**")
    if st.button("💬 Where is my order ORD001?"):        send_sample("Where is my order ORD001?")
    if st.button("💬 Track my order ORD002"):            send_sample("Track my order ORD002")
    if st.button("💬 Status of order ORD003?"):          send_sample("What is the status of ORD003?")
    if st.button("💬 Has ORD004 been delivered?"):       send_sample("Has my order ORD004 been delivered?")

    st.markdown("---")
    st.markdown("**📜 POLICIES & RETURNS**")
    if st.button("💬 What is the return policy?"):       send_sample("What is your return policy?")
    if st.button("💬 How do I get a refund?"):           send_sample("How do I get a refund?")
    if st.button("💬 What is the warranty policy?"):     send_sample("What is the warranty policy?")
    if st.button("💬 How long does shipping take?"):     send_sample("How long does shipping take?")

    st.markdown("---")
    st.markdown("**⚠️ COMPLAINTS**")
    if st.button("💬 My product arrived damaged"):       send_sample("My product arrived damaged")
    if st.button("💬 I received the wrong item"):        send_sample("I received the wrong item")
    if st.button("💬 My order has not arrived"):         send_sample("My order has not arrived yet")
    if st.button("💬 I want to raise a complaint"):      send_sample("I want to raise a complaint")

    st.markdown("---")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("# 🛍️ *AssistIQ* — Customer Assistant")
st.caption("SMART MULTI-AGENT AI · REAL-TIME SUPPORT")
st.markdown("---")

# ── CHAT STATE ────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── WELCOME CARD ──────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;
            justify-content:center;padding:3.5rem 2rem 2.5rem;text-align:center;">
    <div style="width:64px;height:64px;border-radius:18px;
                background:linear-gradient(135deg,#1E3A5F,#2563EB);
                display:flex;align-items:center;justify-content:center;
                font-size:1.8rem;margin-bottom:20px;
                box-shadow:0 8px 24px rgba(37,99,235,0.25);">🛍️</div>
    <div style="font-family:'Playfair Display',serif;font-size:1.9rem;
                font-style:italic;color:#1A202C;margin-bottom:10px;
                letter-spacing:-0.02em;line-height:1.2;font-weight:600;">
        How can I help you today?
    </div>
    <div style="font-size:0.92rem;color:#718096;max-width:400px;
                line-height:1.75;margin-bottom:8px;">
        I specialise in order tracking, product recommendations,
        store policies, and complaint resolution.
    </div>
    <div style="font-size:0.8rem;color:#A0AEC0;margin-bottom:26px;">
        ← Pick a sample question from the sidebar or type below
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
        <div style="background:#EBF4FF;border:1px solid #BEE3F8;border-radius:50px;
                    padding:8px 18px;font-size:0.8rem;color:#2B6CB0;font-weight:600;">
            🛍️ Products</div>
        <div style="background:#F0FFF4;border:1px solid #9AE6B4;border-radius:50px;
                    padding:8px 18px;font-size:0.8rem;color:#276749;font-weight:600;">
            📦 Orders</div>
        <div style="background:#FFFAF0;border:1px solid #FBD38D;border-radius:50px;
                    padding:8px 18px;font-size:0.8rem;color:#975A16;font-weight:600;">
            📜 Policies</div>
        <div style="background:#FFF5F5;border:1px solid #FEB2B2;border-radius:50px;
                    padding:8px 18px;font-size:0.8rem;color:#9B2C2C;font-weight:600;">
            ⚠️ Complaints</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── REPLAY HISTORY ────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── HANDLE INPUT ──────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask me anything about your order, products or policies…")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            bot_reply, latency = call_chat_api(user_input)
        st.markdown(bot_reply)
        if latency is not None:
            st.caption(f"⏱ {latency:.2f}s")
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:0.72rem;color:#A0AEC0;"
    "letter-spacing:0.08em;font-weight:600;text-transform:uppercase;'>"
    "© 2026 AssistIQ &nbsp;·&nbsp; AI Customer Support Platform</p>",
    unsafe_allow_html=True,
)
