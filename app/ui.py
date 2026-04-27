import os
from typing import Optional, Tuple
import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

# ------------------------------------------------------------------ #
#  FIX 3 — API URL from environment variable, fallback for local dev  #
# ------------------------------------------------------------------ #

# NEW
API_URL = os.getenv("ASSISTIQ_API_URL", "https://customer-support-agent-wppl.onrender.com/chat")
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AssistIQ",
    page_icon="🛍️",
    layout="wide"
)

# ------------------------------------------------------------------ #
#  FIX 4 — CSS uses stable data-testid selectors + scoped variables   #
#  All fragile class-name selectors replaced; !important kept only    #
#  where Streamlit's own styles genuinely fight back.                 #
# ------------------------------------------------------------------ #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Serif+Display&display=swap');

/* ── Scoped design tokens ────────────────────────────────────────── */
:root {
    --iq-navy:       #0B1D3A;
    --iq-navy-mid:   #132850;
    --iq-navy-light: #1B3668;
    --iq-accent:     #3D7FFF;
    --iq-accent-dim: rgba(61,127,255,0.12);
    --iq-surface:    #F0F4FF;
    --iq-white:      #FFFFFF;
    --iq-border:     #D0DCFF;
    --iq-text:       #0B1D3A;
    --iq-muted:      #5A6A8A;
    --iq-faint:      #8899BB;
}

/* ── Global font ─────────────────────────────────────────────────── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--iq-surface) !important;
}

/* ── Hide Streamlit chrome ───────────────────────────────────────── */
#MainMenu,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
footer { visibility: hidden !important; display: none !important; }

/* ── Main content padding ────────────────────────────────────────── */
[data-testid="stMain"] .block-container {
    padding: 2rem 2.5rem 5rem !important;
    max-width: 1000px !important;
}

/* ── Page heading ────────────────────────────────────────────────── */
[data-testid="stMain"] h1 {
    font-family: 'DM Serif Display', serif !important;
    font-size: 2.4rem !important;
    font-weight: 400 !important;
    color: var(--iq-navy) !important;
    letter-spacing: -0.02em !important;
    line-height: 1.15 !important;
}

/* ── Dividers ────────────────────────────────────────────────────── */
[data-testid="stMain"] hr {
    border: none !important;
    border-top: 1.5px solid var(--iq-border) !important;
    margin: 1rem 0 !important;
    opacity: 0.8;
}

/* ── Caption (subtitle + latency) ───────────────────────────────── */
[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    font-size: 0.82rem !important;
    color: var(--iq-faint) !important;
    font-style: italic;
    letter-spacing: 0.02em;
}

/* ── SIDEBAR shell ───────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--iq-navy) !important;
    min-width: 240px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(
        180deg, var(--iq-navy) 0%, var(--iq-navy-mid) 55%, var(--iq-navy-light) 100%
    ) !important;
    padding-top: 1.4rem !important;
}

/* ── Sidebar text (lock ALL text nodes to 13px) ──────────────────── */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] div {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    color: #A8BDE6 !important;
    line-height: 1.7 !important;
}
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b { color: #FFFFFF !important; font-weight: 600 !important; }

/* Sidebar headings — section labels */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #FFFFFF !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
    margin: 0 0 8px 0 !important;
    padding: 0 !important;
}
/* Brand title only — larger + mixed case */
[data-testid="stSidebar"] h2:first-of-type {
    font-size: 18px !important;
    text-transform: none !important;
    letter-spacing: -0.01em !important;
    font-weight: 700 !important;
}

/* Sidebar caption */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    font-size: 11px !important;
    color: #6A8AB8 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    font-style: normal !important;
}

/* Sidebar dividers */
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.1) !important;
    margin: 12px 0 !important;
}

/* ── Sidebar buttons ─────────────────────────────────────────────── */
[data-testid="stSidebar"] [data-testid="stButton"] > button {
    width: 100% !important;
    background: var(--iq-accent-dim) !important;
    border: 1px solid rgba(61,127,255,0.30) !important;
    border-radius: 10px !important;
    color: #C8DAFF !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 8px 12px !important;
    margin-bottom: 6px !important;
    text-align: left !important;
    transition: all 0.18s ease !important;
}
[data-testid="stSidebar"] [data-testid="stButton"] > button:hover {
    background: rgba(61,127,255,0.26) !important;
    border-color: rgba(61,127,255,0.65) !important;
    color: #FFFFFF !important;
    transform: translateX(3px) !important;
    box-shadow: 0 4px 16px rgba(61,127,255,0.22) !important;
}
/* Clear Chat button — red tint (last stButton in sidebar) */
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button {
    background: rgba(210,60,60,0.10) !important;
    border-color: rgba(210,60,60,0.28) !important;
    color: #FFAAAA !important;
}
[data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button:hover {
    background: rgba(210,60,60,0.25) !important;
    border-color: rgba(210,60,60,0.60) !important;
    color: #FFFFFF !important;
}

/* ── Chat messages ───────────────────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 4px 0 !important;
}
[data-testid="stChatMessage"] p {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    line-height: 1.78 !important;
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] {
    background: linear-gradient(135deg, #3D7FFF 0%, #1A54E0 100%) !important;
    border-radius: 18px 18px 4px 18px !important;
    padding: 12px 18px !important;
    box-shadow: 0 4px 16px rgba(61,127,255,0.30) !important;
    max-width: 80% !important;
    margin-left: auto !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"])
    [data-testid="stMarkdownContainer"] p { color: #FFFFFF !important; }

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] {
    background: var(--iq-white) !important;
    border: 1px solid var(--iq-border) !important;
    border-radius: 18px 18px 18px 4px !important;
    padding: 12px 18px !important;
    box-shadow: 0 2px 10px rgba(11,29,58,0.07) !important;
    max-width: 80% !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"])
    [data-testid="stMarkdownContainer"] p { color: var(--iq-text) !important; }

/* ── Chat input ──────────────────────────────────────────────────── */
[data-testid="stChatInput"] {
    border-radius: 50px !important;
    border: 2px solid #C8D8FF !important;
    background: var(--iq-white) !important;
    box-shadow: 0 4px 20px rgba(11,29,58,0.10) !important;
    padding: 4px 6px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--iq-accent) !important;
    box-shadow: 0 0 0 4px rgba(61,127,255,0.12),
                0 4px 20px rgba(11,29,58,0.10) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.97rem !important;
    color: var(--iq-text) !important;
    padding: 10px 14px !important;
    line-height: 1.6 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #9AAAD0 !important;
    font-style: italic !important;
}
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #3D7FFF 0%, #1A54E0 100%) !important;
    border-radius: 50% !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(61,127,255,0.40) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
[data-testid="stChatInput"] button:hover {
    transform: scale(1.09) !important;
    box-shadow: 0 6px 20px rgba(61,127,255,0.55) !important;
}

/* ── Spinner ─────────────────────────────────────────────────────── */
[data-testid="stSpinner"] p {
    font-size: 0.9rem !important;
    color: var(--iq-muted) !important;
    font-style: italic !important;
}

/* ── Scrollbar ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--iq-border); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: #A0B8E8; }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  HELPER — robust API call                                           #
#  FIX 2 — handles connection errors, timeouts AND bad HTTP status   #
# ------------------------------------------------------------------ #
def call_chat_api(message: str) -> Tuple[str, Optional[float]]:
    """
    Returns (reply_text, latency_seconds_or_None).
    Never raises — all error paths return a user-friendly string.
    """
    try:
        resp = requests.post(
            API_URL,
            json={"message": message},
            timeout=30,          # fail fast rather than hang forever
        )
        resp.raise_for_status()  # raises HTTPError for 4xx / 5xx responses
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
        # JSON decode failure
        return "⚠️ Received an unexpected response from the server.", None

    except RequestException as e:
        # Catch-all for any other requests-level error
        return f"⚠️ Network error: {e}", None


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🛍️ AssistIQ")
    st.caption("INTELLIGENT SUPPORT SYSTEM")

    st.markdown("---")

    st.markdown("**📘 USER GUIDE**")
    st.markdown("""
&nbsp;• Ask about **products** → recommendations\n
&nbsp;• Ask about **orders** → status & tracking\n
&nbsp;• Ask about **policies** → returns, refunds\n
&nbsp;• Report **issues** → complaint registration
""")

    st.markdown("---")

    st.markdown("**ℹ️ ABOUT**")
    st.markdown("""
A **multi-agent AI** customer support system.

**Features:**\n
&nbsp;· Product recommendations (RAG)\n
&nbsp;· Order tracking (DB)\n
&nbsp;· Policy Q&A\n
&nbsp;· Complaint management

Powered by LLM + FastAPI + Streamlit
""")

    st.markdown("---")

    st.markdown("**🚀 DEMO SCENARIOS**")

    if st.button("🛍️ Product Recommendation"):
        st.session_state.messages.append({
            "role": "user",
            "content": "Recommend a good speaker"
        })
        st.rerun()

    if st.button("📦 Track Order"):
        st.session_state.messages.append({
            "role": "user",
            "content": "Where is my order ORD123?"
        })
        st.rerun()

    if st.button("📜 Refund Policy"):
        st.session_state.messages.append({
            "role": "user",
            "content": "What is your refund policy?"
        })
        st.rerun()

    if st.button("⚠️ Raise Complaint"):
        st.session_state.messages.append({
            "role": "user",
            "content": "My product is damaged"
        })
        st.rerun()

    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("# 🛍️ AssistIQ Customer Assistant")
st.caption("Smart multi-agent AI customer support platform")
st.markdown("---")

# ---------------- CHAT STATE ----------------
# FIX 1 — each message stores ONLY role + content (no latency).
# Latency is displayed live but never written to history, so
# replaying history never shows stale/duplicate latency lines.
if "messages" not in st.session_state:
    st.session_state.messages = []   # [{"role": str, "content": str}]

# ---------------- WELCOME CARD ----------------
if not st.session_state.messages:
    st.markdown("""
<div style="display:flex;flex-direction:column;align-items:center;
            justify-content:center;padding:3.5rem 2rem 2.5rem;text-align:center;">
    <div style="font-size:3rem;margin-bottom:16px;">💬</div>
    <div style="font-family:'DM Serif Display',serif;font-size:1.7rem;
                color:#0B1D3A;margin-bottom:10px;font-weight:400;">
        How can I help you today?
    </div>
    <div style="font-size:0.97rem;color:#5A6A8A;max-width:420px;
                line-height:1.7;margin-bottom:24px;">
        I can help you track orders, find products, check policies, or handle
        complaints — just ask anything or pick a scenario from the sidebar.
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center;">
        <span style="background:#FFFFFF;border:1px solid #D0DCFF;border-radius:50px;
                     padding:8px 18px;font-size:0.84rem;color:#5A6A8A;font-weight:500;">
            🛍️ Recommend a product</span>
        <span style="background:#FFFFFF;border:1px solid #D0DCFF;border-radius:50px;
                     padding:8px 18px;font-size:0.84rem;color:#5A6A8A;font-weight:500;">
            📦 Track my order</span>
        <span style="background:#FFFFFF;border:1px solid #D0DCFF;border-radius:50px;
                     padding:8px 18px;font-size:0.84rem;color:#5A6A8A;font-weight:500;">
            📜 Refund policy</span>
        <span style="background:#FFFFFF;border:1px solid #D0DCFF;border-radius:50px;
                     padding:8px 18px;font-size:0.84rem;color:#5A6A8A;font-weight:500;">
            ⚠️ Report issue</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- REPLAY HISTORY ----------------
# FIX 1 — history contains only role + content; latency is never stored here
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- HANDLE NEW INPUT ----------------
user_input = st.chat_input("Ask anything...")

if user_input:
    # 1. Show + store user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Call API and display assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            bot_reply, latency = call_chat_api(user_input)

        # Render reply
        st.markdown(bot_reply)

        # FIX 1 — latency shown live here but NOT added to session_state
        if latency is not None:
            st.caption(f"⏱️ Response time: {latency:.2f} sec")

    # FIX 1 — store ONLY content, no latency key
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center;font-size:0.78rem;color:#8899BB;letter-spacing:0.04em;'>"
    "© 2026 AssistIQ &nbsp;·&nbsp; AI Customer Support Platform"
    "</p>",
    unsafe_allow_html=True,
)
