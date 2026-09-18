import streamlit as st
import json
import uuid
from pathlib import Path
from datetime import datetime
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage
from operator import add

# ─── Config ───────────────────────────────────────────────────────────────────
CHATS_FILE = "chats.json"
CHATS_DIR = Path("chat_history")
CHATS_DIR.mkdir(exist_ok=True)

llm = ChatOllama(model="llama3.2:1b")

# ─── Graph ────────────────────────────────────────────────────────────────────
class chatstate(TypedDict):
    mesage: Annotated[list, add]

def chat_node(state: chatstate) -> chatstate:
    response = llm.invoke(state["mesage"])
    return {"mesage": [AIMessage(content=response.content)]}

graph = StateGraph(chatstate)
graph.add_node("chat", chat_node)
graph.add_edge(START, "chat")
graph.add_edge("chat", END)

# ─── Persistence ──────────────────────────────────────────────────────────────
def load_chats():
    p = Path(CHATS_FILE)
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return []

def save_chats(chats):
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f, indent=2, default=str)

def load_messages(chat_id):
    p = CHATS_DIR / f"{chat_id}.json"
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return []

def save_messages(chat_id, messages):
    with open(CHATS_DIR / f"{chat_id}.json", "w") as f:
        json.dump(messages, f, indent=2)

# ─── Session State ────────────────────────────────────────────────────────────
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── Design System ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ChatBot",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #09090b;
    --bg-secondary: #0f0f12;
    --bg-tertiary: #16161a;
    --bg-elevated: #1c1c21;
    --bg-hover: #222228;
    --bg-active: #2a2a31;
    --bg-input: #111115;
    --border-subtle: rgba(255,255,255,0.06);
    --border-default: rgba(255,255,255,0.1);
    --border-focus: rgba(99, 102, 241, 0.5);
    --text-primary: #f4f4f5;
    --text-secondary: #a1a1aa;
    --text-muted: #63636e;
    --accent: #6366f1;
    --accent-hover: #818cf8;
    --accent-dim: rgba(99, 102, 241, 0.12);
    --accent-glow: rgba(99, 102, 241, 0.25);
    --success: #22c55e;
    --danger: #ef4444;
    --gradient-1: linear-gradient(135deg, #6366f1, #a855f7, #ec4899);
    --gradient-2: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
    --gradient-bg: radial-gradient(ellipse at 50% 0%, rgba(99, 102, 241, 0.08) 0%, transparent 60%);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.4);
    --shadow-lg: 0 12px 40px rgba(0,0,0,0.5);
    --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.15);
    --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --transition: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.stApp {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: var(--font) !important;
}

.stApp::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 50vh;
    background: var(--gradient-bg);
    pointer-events: none;
    z-index: 0;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

/* ─── Sidebar ──────────────────────────────────────────────────────────── */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 4px 0 20px 0;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 16px;
}

.sidebar-brand-icon {
    width: 36px;
    height: 36px;
    background: var(--gradient-1);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    box-shadow: var(--shadow-glow);
}

.sidebar-brand h2 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: -0.03em;
}

.sidebar-brand p {
    font-size: 11px;
    color: var(--text-muted);
    margin: 2px 0 0 0;
    letter-spacing: 0.02em;
}

/* ─── Buttons ──────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 10px 16px !important;
    transition: all var(--transition) !important;
    letter-spacing: -0.01em !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: var(--accent-hover) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35) !important;
}

.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    font-family: var(--font) !important;
    font-weight: 400 !important;
    font-size: 12px !important;
    padding: 8px 12px !important;
    text-align: left !important;
    transition: all var(--transition) !important;
}

.stButton > button[data-testid="stBaseButton-secondary"]:hover {
    background: var(--bg-hover) !important;
    border-color: var(--border-default) !important;
    color: var(--text-primary) !important;
}

/* ─── Chat Item ────────────────────────────────────────────────────────── */
.chat-item {
    padding: 10px 12px;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition);
    margin-bottom: 2px;
    border: 1px solid transparent;
}

.chat-item:hover {
    background: var(--bg-hover);
}

.chat-item.active {
    background: var(--accent-dim);
    border-color: rgba(99, 102, 241, 0.2);
}

.chat-item-title {
    font-size: 13px;
    font-weight: 500;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.chat-item-meta {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 3px;
}

/* ─── Welcome / Empty State ────────────────────────────────────────────── */
.main-header {
    text-align: center;
    padding: 60px 20px 40px;
    position: relative;
    z-index: 1;
}

.main-header h1 {
    font-size: 36px;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.04em;
    margin-bottom: 10px;
    line-height: 1.2;
}

.main-header h1 .gradient-text {
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.main-header > p {
    font-size: 15px;
    color: var(--text-muted);
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.6;
}

.welcome-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    max-width: 580px;
    margin: 36px auto 0;
}

.welcome-card {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 20px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
}

.welcome-card:hover {
    border-color: var(--border-default);
    background: var(--bg-elevated);
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
}

.welcome-card-icon {
    width: 36px;
    height: 36px;
    background: var(--accent-dim);
    border-radius: var(--radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 12px;
}

.welcome-card-title {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.welcome-card-desc {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.5;
}

/* ─── Chat Messages ────────────────────────────────────────────────────── */
.chat-container {
    max-width: 780px;
    margin: 0 auto;
    padding: 24px 20px;
}

.message {
    display: flex;
    gap: 14px;
    margin-bottom: 28px;
    animation: messageIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes messageIn {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.message-avatar {
    width: 34px;
    height: 34px;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 2px;
}

.message-avatar.user {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
}

.message-avatar.assistant {
    background: var(--gradient-1);
    box-shadow: var(--shadow-glow);
}

.message-content {
    flex: 1;
    min-width: 0;
}

.message-role {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 6px;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 8px;
}

.message-role .tag {
    font-size: 10px;
    font-weight: 500;
    color: var(--text-muted);
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
    letter-spacing: 0.02em;
}

.message-text {
    font-size: 14px;
    color: var(--text-secondary);
    line-height: 1.7;
    word-wrap: break-word;
}

.message-text code {
    background: var(--bg-tertiary);
    padding: 2px 7px;
    border-radius: 5px;
    font-size: 13px;
    color: var(--accent-hover);
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    border: 1px solid var(--border-subtle);
}

.message-text pre {
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 18px;
    overflow-x: auto;
    margin: 14px 0;
}

.message-text pre code {
    background: none;
    padding: 0;
    border: none;
    color: var(--text-secondary);
    font-size: 13px;
    line-height: 1.6;
}

/* ─── Typing Indicator ─────────────────────────────────────────────────── */
.typing-indicator {
    display: flex;
    gap: 5px;
    padding: 14px 18px;
    background: var(--bg-tertiary);
    border-radius: var(--radius-lg);
    width: fit-content;
    border: 1px solid var(--border-subtle);
}

.typing-dot {
    width: 7px;
    height: 7px;
    background: var(--text-muted);
    border-radius: 50%;
    animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
    0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
    30% { transform: translateY(-6px); opacity: 1; }
}

/* ─── Chat Input ───────────────────────────────────────────────────────── */
.stChatInput {
    border-radius: var(--radius-lg) !important;
}

.stChatInput > div {
    background: var(--bg-tertiary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stChatInput > div:focus-within {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px var(--accent-dim), var(--shadow-sm) !important;
}

.stChatInput textarea {
    font-family: var(--font) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important;
}

/* ─── Spinner ──────────────────────────────────────────────────────────── */
.stSpinner > div {
    border-color: var(--accent) transparent transparent transparent !important;
}

/* ─── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: var(--border-default);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* ─── Streamlit Overrides ──────────────────────────────────────────────── */
.stDeployButton { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

div[data-testid="stToolbar"] { display: none; }
div[data-testid="stDecoration"] { display: none; }

/* ─── Empty State ──────────────────────────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
}

.empty-state-icon {
    width: 64px;
    height: 64px;
    background: var(--accent-dim);
    border-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin: 0 auto 20px;
}

.empty-state h3 {
    font-size: 17px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.empty-state p {
    font-size: 13px;
    color: var(--text-muted);
    max-width: 320px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ─── Timestamp ────────────────────────────────────────────────────────── */
.message-time {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 8px;
}

/* ─── Divider ──────────────────────────────────────────────────────────── */
.sidebar-divider {
    border: none;
    border-top: 1px solid var(--border-subtle);
    margin: 14px 0;
}

/* ─── Section Label ────────────────────────────────────────────────────── */
.sidebar-section {
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0 4px;
    margin-bottom: 10px;
}

/* ─── Delete Button ────────────────────────────────────────────────────── */
.delete-btn {
    background: none;
    border: none;
    color: var(--text-muted);
    cursor: pointer;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 12px;
    transition: all var(--transition);
    opacity: 0;
}

.chat-item-wrapper:hover .delete-btn {
    opacity: 1;
}

.delete-btn:hover {
    color: var(--danger);
    background: rgba(239, 68, 68, 0.1);
}

/* ─── Status Bar ───────────────────────────────────────────────────────── */
.status-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 6px 0;
    font-size: 11px;
    color: var(--text-muted);
    border-top: 1px solid var(--border-subtle);
    margin-top: 16px;
}

.status-dot {
    width: 6px;
    height: 6px;
    background: var(--success);
    border-radius: 50%;
    animation: pulse 2s infinite;
}

/* ─── Model Badge ──────────────────────────────────────────────────────── */
.model-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--bg-tertiary);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-full);
    padding: 4px 10px;
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 12px;
}

.model-badge .dot {
    width: 5px;
    height: 5px;
    background: var(--accent);
    border-radius: 50%;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">✦</div>
            <div>
                <h2>ChatBot</h2>
                <p>LangGraph + Ollama</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if st.button("+ New Chat", use_container_width=True, type="primary"):
        new_id = str(uuid.uuid4())
        chats = load_chats()
        chats.insert(0, {"id": new_id, "title": "New Chat", "created_at": str(datetime.now())})
        save_chats(chats)
        st.session_state.current_chat = new_id
        st.session_state.messages = []
        st.rerun()

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Recent Chats</div>', unsafe_allow_html=True)

    chats = load_chats()
    for chat in chats:
        is_active = chat["id"] == st.session_state.current_chat
        active_class = "active" if is_active else ""
        title = chat["title"]
        if title == "New Chat":
            title = "New Chat"
        created = chat.get("created_at", "")

        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
                <div class="chat-item {active_class}">
                    <div class="chat-item-title">{'● ' if is_active else ''}{title}</div>
                    <div class="chat-item-meta">{created[:10] if created else ''}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            if st.button("🗑", key=f"del_{chat['id']}", help="Delete chat"):
                chats_to_delete = load_chats()
                chats_to_delete = [c for c in chats_to_delete if c["id"] != chat["id"]]
                save_chats(chats_to_delete)
                chat_file = CHATS_DIR / f"{chat['id']}.json"
                if chat_file.exists():
                    chat_file.unlink()
                if st.session_state.current_chat == chat["id"]:
                    st.session_state.current_chat = None
                    st.session_state.messages = []
                st.rerun()

        if st.button("Open", key=f"btn_{chat['id']}", use_container_width=True, type="secondary"):
            st.session_state.current_chat = chat["id"]
            st.session_state.messages = load_messages(chat["id"])
            st.rerun()

    if not chats:
        st.markdown("""
            <div style="text-align:center; padding: 32px 0; color: var(--text-muted); font-size: 13px;">
                No chats yet.<br>Start a new conversation.
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class="status-bar">
            <span class="status-dot"></span>
            Online
        </div>
    """, unsafe_allow_html=True)

# ─── Normalize Messages ──────────────────────────────────────────────────────
normalized = []
for msg in st.session_state.messages:
    if isinstance(msg, dict):
        normalized.append(msg)
    elif isinstance(msg, HumanMessage):
        normalized.append({"role": "user", "content": msg.content})
    elif isinstance(msg, AIMessage):
        normalized.append({"role": "assistant", "content": msg.content})
st.session_state.messages = normalized

# ─── Main Content ────────────────────────────────────────────────────────────
if not st.session_state.current_chat:
    st.markdown("""
        <div class="main-header">
            <h1>What can I help with? <span class="gradient-text">✦</span></h1>
            <p>Start a conversation or pick up where you left off.</p>
            <div class="welcome-grid">
                <div class="welcome-card">
                    <div class="welcome-card-icon">💡</div>
                    <div class="welcome-card-title">Explain concepts</div>
                    <div class="welcome-card-desc">Break down complex topics into simple ideas</div>
                </div>
                <div class="welcome-card">
                    <div class="welcome-card-icon">✍️</div>
                    <div class="welcome-card-title">Write content</div>
                    <div class="welcome-card-desc">Draft emails, articles, and creative text</div>
                </div>
                <div class="welcome-card">
                    <div class="welcome-card-icon">🛠️</div>
                    <div class="welcome-card-title">Debug code</div>
                    <div class="welcome-card-desc">Find and fix issues in your codebase</div>
                </div>
                <div class="welcome-card">
                    <div class="welcome-card-icon">🧠</div>
                    <div class="welcome-card-title">Brainstorm ideas</div>
                    <div class="welcome-card-desc">Generate and refine creative concepts</div>
                </div>
            </div>
            <div class="model-badge">
                <span class="dot"></span>
                llama3.2:1b via Ollama
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    if st.session_state.messages:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            role = msg["role"]
            avatar_class = "user" if role == "user" else "assistant"
            avatar = "👤" if role == "user" else "✦"
            label = "You" if role == "user" else "Assistant"
            tag = "" if role == "user" else '<span class="tag">AI</span>'

            content = msg["content"].replace("\n", "<br>")

            st.markdown(f"""
                <div class="message">
                    <div class="message-avatar {avatar_class}">{avatar}</div>
                    <div class="message-content">
                        <div class="message-role">{label} {tag}</div>
                        <div class="message-text">{content}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Message ChatBot...", disabled=st.session_state.current_chat is None):
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_messages(st.session_state.current_chat, st.session_state.messages)

        chats = load_chats()
        chat = next((c for c in chats if c["id"] == st.session_state.current_chat), None)
        if chat and chat["title"] == "New Chat":
            title = prompt[:35] + ("..." if len(prompt) > 35 else "")
            chat["title"] = title
            save_chats(chats)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                with SqliteSaver.from_conn_string("chat_bot.db") as connection_db:
                    workflow = graph.compile(checkpointer=connection_db)
                    result = workflow.invoke(
                        {"mesage": [HumanMessage(content=prompt)]},
                        config={"configurable": {"thread_id": st.session_state.current_chat}},
                    )
            response = result["mesage"][-1]
            st.write(response.content)
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            save_messages(st.session_state.current_chat, st.session_state.messages)
