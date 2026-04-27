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
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@300;400;500;600;700&display=swap');

:root {
    --c-bg:          #F7F8FC;
    --c-surface:     #FFFFFF;
    --c-navy:        #0D1B2A;
    --c-accent:      #2563EB;
    --c-accent-glow: rgba(37,99,235,0.15);
    --c-border:      #E2E8F4;
    --c-border-2:    #CBD5E8;
    --c-text:        #0D1B2A;
    --c-muted:       #64748B;
    --c-faint:       #94A3B8;
    --shadow-sm:     0 2px 8px rgba(13,27,42,0.08);
    --shadow-md:     0 6px 24px rgba(13,27,42,0.10);
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    font-family: 'Geist', sans-serif !important;
    background: var(--c-bg) !important;
    color: var(--c-text) !important;
}

#MainMenu,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer { visibility: hidden !important; display: none !important; }

[data-testid="stMain"] .block-container {
    padding: 2.5rem 3rem 6rem !important;
    max-width: 960px !important;
}

[data-testid="stMain"] h1 {
    font-family: 'Instrument Serif', serif !important;
    font-size: 2.6rem !important;
    font-weight: 400 !important;
    font-style: italic !important;
    color: var(--c-navy) !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
    margin-bottom: 0 !important;
}

[data-testid="stMain"] hr {
    border: none !important;
    border-top: 1px solid var(--c-border) !important;
    margin: 1.2rem 0 !important;
}

[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    font-size: 0.75rem !important;
    color: var(--c-faint) !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-style: normal !important;
}

/* ── SIDEBAR SHELL ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0D1B2A !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(
        160deg, #0D1B2A 0%, #162032 40%, #1A2A42 100%
    ) !important;
    padding-top: 1.6rem !important;
}

/* ── SIDEBAR TEXT — aggressive targeting of every node ───────────── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] *:not(button):not(h1):not(h2):not(h3):not(strong):not(b) {
    font-family: 'Geist', sans-serif !important;
    color: #94AECF !important;
}

[data-testid="stSidebar"] p {
    font-size: 12.5px !important;
    font-weight: 400 !important;
    color: #94AECF !important;
    line-height: 1.72 !important;
}

[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* ── Sidebar headings ── */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Geist', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    color: #3A5882 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    margin: 0 0 8px 0 !important;
    padding: 0 !important;
    background: transparent !important;
}

/* Brand heading override */
[data-testid="stSidebar"] h2:first-of-type {
    font-family: 'Instrument Serif', serif !important;
    font-size: 22px !important;
    font-style: italic !important;
    text-transform: none !important;
    letter-spacing: -0.01em !important;
    font-weight: 400 !important;
    color: #FFFFFF !important;
    margin-bottom: 2px !important;
}

/* ── Sidebar caption ── */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    font-size: 10px !important;
    color: #3A5882 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    font-style: normal !important;
}

/* ── Sidebar hr ── */
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.08) !important;
    margin: 14px 0 !important;
}

/* ── Sidebar buttons ── */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    width: 100% !important;
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 7px !important;
    color: #94AECF !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    font-family: 'Geist', sans-serif !important;
    padding: 8px 12px !important;
    margin-bottom: 4px !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
    line-height: 1.5 !important;
    white-space: normal !important;
    height: auto !important;
    min-height: unset !important;
}

/* Force button inner text colour */
[data-testid="stSidebar"] [data-testid="stButton"] > button *,
[data-testid="stSidebar"] [data-testid="stButton"] > button p,
[data-testid="stSidebar"] [data-testid="stButton"] > button div,
[data-testid="stSidebar"] [data-testid="stButton"] > button span {
    color: #94AECF !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    font-family: 'Geist', sans-serif !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: rgba(37,99,235,0.18) !important;
    border-color: rgba(37,99,235,0.40) !important;
    color: #FFFFFF !important;
    transform: translateX(3px) !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] > button:hover *,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover p,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover div,
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover span {
    color: #FFFFFF !important;
}

/* Clear Chat — red tint (last button) */
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button,
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button * {
    background: rgba(239,68,68,0.08) !important;
    border-color: rgba(239,68,68,0.20) !important;
    color: #F87171 !important;
    font-weight: 500 !important;
    font-size: 12.5px !important;
}
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button:hover,
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button:hover * {
    background: rgba(239,68,68,0.20) !important;
    border-color: rgba(239,68,68,0.50) !important;
    color: #FFFFFF !important;
}

/* ── CHAT MESSAGES ───────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 5px 0 !important;
}
[data-testid="stChatMessage"] p {
    font-family: 'Geist', sans-serif !important;
    font-size: 0.94rem !important;
    line-height: 1.8 !important;
    margin: 0 !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] {
    background: #0D1B2A !important;
    border-radius: 20px 20px 4px 20px !important;
    padding: 13px 19px !important;
    box-shadow: var(--shadow-md) !important;
    max-width: 78% !important;
    margin-left: auto !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] p { color: #E2EAF4 !important; }

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] {
    background: #FFFFFF !important;
    border: 1px solid var(--c-border) !important;
    border-radius: 4px 20px 20px 20px !important;
    padding: 13px 19px !important;
    box-shadow: var(--shadow-sm) !important;
    max-width: 78% !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] p { color: var(--c-text) !important; }

/* Latency caption */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stCaptionContainer"] p {
    font-size: 0.72rem !important;
    color: var(--c-faint) !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    font-style: normal !important;
}

/* ── CHAT INPUT ──────────────────────────────────────────────────── */
[data-testid="stChatInput"] {
    border-radius: 50px !important;
    border: 1.5px solid var(--c-border-2) !important;
    background: #FFFFFF !important;
    box-shadow: var(--shadow-md) !important;
    padding: 4px 6px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--c-accent) !important;
    box-shadow: 0 0 0 3px var(--c-accent-glow), var(--shadow-md) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Geist', sans-serif !important;
    font-size: 0.93rem !important;
    color: var(--c-text) !important;
    padding: 12px 16px !important;
    line-height: 1.6 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--c-faint) !important;
    font-weight: 300 !important;
}
[data-testid="stChatInput"] button {
    background: #0D1B2A !important;
    border-radius: 50% !important;
    border: none !important;
    transition: all 0.15s !important;
}
[data-testid="stChatInput"] button:hover {
    background: var(--c-accent) !important;
    transform: scale(1.08) !important;
    box-shadow: 0 4px 16px rgba(37,99,235,0.40) !important;
}

/* ── SPINNER ─────────────────────────────────────────────────────── */
[data-testid="stSpinner"] p {
    font-size: 0.85rem !important;
    color: var(--c-muted) !important;
    font-weight: 400 !important;
}
/* ── Force sidebar always visible ───────────────────────────────── */
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
}
[data-testid="stSidebar"][aria-expanded="false"] {
    display: flex !important;
    width: 258px !important;
    min-width: 258px !important;
}
/* ── SCROLLBAR ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--c-border-2); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: var(--c-muted); }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  HELPER — robust API call                                           #
# ------------------------------------------------------------------ #
def call_chat_api(message: str) -> Tuple[str, Optional[float]]:
    try:
        resp = requests.post(API_URL, json={"message": message}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "⚠️ The server returned an empty response."), \
               data.get("latency")
    except ConnectionError:
        return "⚠️ Cannot reach the server. Please check that the backend is running.", None
    except Timeout:
        return "⚠️ The request timed out. The server may be overloaded — please try again.", None
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        return f"⚠️ Server error (HTTP {status}). Please try again or contact support.", None
    except ValueError:
        return "⚠️ Received an unexpected response from the server.", None
    except RequestException as e:
        return f"⚠️ Network error: {e}", None


def send_sample(question: str):
    st.session_state.messages.append({"role": "user", "content": question})
    st.rerun()


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🛍️ AssistIQ")
    st.caption("Customer Intelligence Platform")
    st.markdown("---")

    st.markdown("**🛍️ PRODUCT RECOMMENDATIONS**")
    if st.button("Recommend a good Bluetooth speaker"):
        send_sample("Recommend a good Bluetooth speaker")
    if st.button("Best budget laptop under ₹50,000"):
        send_sample("Best budget laptop under ₹50,000")
    if st.button("Suggest noise-cancelling headphones"):
        send_sample("Suggest noise-cancelling headphones")
    if st.button("Best mobile phone under ₹30,000"):
        send_sample("Best mobile phone under ₹30,000")

    st.markdown("---")

    st.markdown("**📦 ORDER TRACKING**")
    if st.button("Where is my order ORD001?"):
        send_sample("Where is my order ORD001?")
    if st.button("Track my order ORD002"):
        send_sample("Track my order ORD002")
    if st.button("What is the status of ORD003?"):
        send_sample("What is the status of ORD003?")
    if st.button("Has my order ORD004 been delivered?"):
        send_sample("Has my order ORD004 been delivered?")

    st.markdown("---")

    st.markdown("**📜 POLICIES & RETURNS**")
    if st.button("What is your return policy?"):
        send_sample("What is your return policy?")
    if st.button("How do I get a refund?"):
        send_sample("How do I get a refund?")
    if st.button("What is the warranty policy?"):
        send_sample("What is the warranty policy?")
    if st.button("How long does shipping take?"):
        send_sample("How long does shipping take?")

    st.markdown("---")

    st.markdown("**⚠️ COMPLAINTS**")
    if st.button("My product arrived damaged"):
        send_sample("My product arrived damaged")
    if st.button("I received the wrong item"):
        send_sample("I received the wrong item")
    if st.button("My order has not arrived yet"):
        send_sample("My order has not arrived yet")
    if st.button("I want to raise a complaint"):
        send_sample("I want to raise a complaint")

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ---------------- HEADER ----------------
st.markdown("# 🛍️ *AssistIQ* — Customer Assistant")
st.caption("SMART MULTI-AGENT AI · REAL-TIME SUPPORT")
st.markdown("---")

# ---------------- CHAT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- WELCOME CARD ----------------
if not st.session_state.messages:
    st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;
            justify-content:center;padding:4rem 2rem 3rem;text-align:center;">
    <div style="width:64px;height:64px;border-radius:20px;
                background:linear-gradient(135deg,#0D1B2A,#1E3A5F);
                display:flex;align-items:center;justify-content:center;
                font-size:1.8rem;margin-bottom:24px;
                box-shadow:0 8px 32px rgba(13,27,42,0.18);">🛍️</div>
    <div style="font-family:'Instrument Serif',serif;font-size:2rem;
                font-style:italic;color:#0D1B2A;margin-bottom:10px;
                letter-spacing:-0.02em;line-height:1.2;">
        How can I help you today?
    </div>
    <div style="font-size:0.92rem;color:#64748B;max-width:420px;
                line-height:1.75;margin-bottom:10px;font-weight:400;">
        I specialise in order tracking, product recommendations,
        store policies, and complaint resolution.
    </div>
    <div style="font-size:0.8rem;color:#94A3B8;margin-bottom:28px;">
        ← Pick a sample question from the sidebar or type below
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
        <div style="background:#FFFFFF;border:1px solid #E2E8F4;border-radius:50px;
                    padding:9px 18px;font-size:0.8rem;color:#475569;font-weight:500;
                    box-shadow:0 1px 4px rgba(13,27,42,.06);">🛍️ Products</div>
        <div style="background:#FFFFFF;border:1px solid #E2E8F4;border-radius:50px;
                    padding:9px 18px;font-size:0.8rem;color:#475569;font-weight:500;
                    box-shadow:0 1px 4px rgba(13,27,42,.06);">📦 Orders</div>
        <div style="background:#FFFFFF;border:1px solid #E2E8F4;border-radius:50px;
                    padding:9px 18px;font-size:0.8rem;color:#475569;font-weight:500;
                    box-shadow:0 1px 4px rgba(13,27,42,.06);">📜 Policies</div>
        <div style="background:#FFFFFF;border:1px solid #E2E8F4;border-radius:50px;
                    padding:9px 18px;font-size:0.8rem;color:#475569;font-weight:500;
                    box-shadow:0 1px 4px rgba(13,27,42,.06);">⚠️ Complaints</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- REPLAY HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- HANDLE NEW INPUT ----------------
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

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:0.72rem;color:#94A3B8;"
    "letter-spacing:0.08em;font-weight:500;text-transform:uppercase;'>"
    "© 2026 AssistIQ &nbsp;·&nbsp; AI Customer Support Platform"
    "</p>",
    unsafe_allow_html=True,
)
