import streamlit as st
from RAG_O import RecipeRAG
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="ChefBot RAG", page_icon="🍳", layout="wide")

# ---------------- Persistent bot ----------------
if "bot" not in st.session_state:
    st.session_state.bot = RecipeRAG()

bot = st.session_state.bot

# ---------------- Chat area (top) ----------------
st.title("🍳 ChefBot — AI Recipe RAG Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- Chat input ----------------
user_msg = st.chat_input("Ask anything about cooking...")

# ============================================================
# IMPORTANT: update memory BEFORE rendering sidebar
# ============================================================
if user_msg:
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": user_msg})

    # Get assistant reply (this updates bot.memory)
    reply = bot.chat(user_msg)

    # Add assistant reply to UI
    st.session_state.messages.append({"role": "assistant", "content": reply})

    st.rerun()   # rerun to refresh sidebar immediately

# ---------------- Sidebar (rendered AFTER updates) ----------------
with st.sidebar:
    st.header("🧠 Conversation Memory (Live)")

    memory = bot.memory.get()
    if memory.strip():
        st.write(memory)
    else:
        st.write("No memory yet.")

    st.header("🥣 Ingredient Recipe Generator")
    ing = st.text_area("Enter ingredients:")
    if st.button("Generate Recipe"):
        st.write(bot.generate_recipe(ing))