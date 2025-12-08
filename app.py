# app.py
import streamlit as st
from backend.user_database import init_db
from backend.auth import create_user, authenticate_user
from RAG_O import RecipeRAG
from rag.memory import DBMemory
from dotenv import load_dotenv
import time
import google.generativeai as genai
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

init_db()

st.set_page_config(page_title="ChefBot RAG", page_icon="🍳", layout="wide")
if "bot" not in st.session_state:
    st.session_state.bot = RecipeRAG()

bot = st.session_state.bot
dbmem = bot.memory  # DBMemory instance

# ----------------- Authentication UI -----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

with st.sidebar:
    st.header("Account")
    if st.session_state.user_id:
        st.write(f"Signed in as **{st.session_state.username}**")
        if st.button("Sign out"):
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
        if st.button("Clear my memory"):
            dbmem.clear_user(st.session_state.user_id)
            st.success("Cleared.")
            st.rerun()
        st.markdown("---")
        st.header("My Memory")
        st.write(dbmem.combined_context(st.session_state.user_id))
    else:
        # login / signup forms
        login_tab, signup_tab = st.tabs(["Login", "Sign up"])
        with login_tab:
            uname = st.text_input("Username", key="li_user")
            pwd = st.text_input("Password", type="password", key="li_pwd")
            if st.button("Login"):
                user = authenticate_user(uname, pwd)
                if user:
                    st.session_state.user_id = user.id
                    st.session_state.username = user.username
                    st.success("Logged in.")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        with signup_tab:
            su_uname = st.text_input("Choose username", key="su_user")
            su_pwd = st.text_input("Choose password", type="password", key="su_pwd")
            if st.button("Create account"):
                try:
                    user = create_user(su_uname, su_pwd)
                    st.success("Account created. Please login.")
                except ValueError as e:
                    st.error(str(e))

# ---------------- Main Chat Area ----------------
st.title("🍳 ChefBot for Me")
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

# Chat input
query = st.chat_input("Ask about recipes, ingredients, or type 'help'...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    user_id = st.session_state.user_id
    # call RAG.chat with user_id (None if anonymous)
    reply = bot.chat(query, user_id=user_id)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
