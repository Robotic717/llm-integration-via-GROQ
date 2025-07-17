# General Chat Bot page
# Handles chat interactions, personality selection, and per-page history
import streamlit as st
from groq import Groq
import instructor
from pydantic import BaseModel, Field
from typing import List

# Set up the Streamlit page configuration
st.set_page_config(
    page_title='General Chat Bot',
    page_icon=':material/chat:'
)

# Sidebar section for API key input
st.sidebar.write("## API Key")

# Initialize API key in session state if not present
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# Input box for user to enter their GROQ API key
api_key = st.sidebar.text_input(
    "Enter your GROQ API Key:",
    value=st.session_state.api_key,
    type="password",
    placeholder="gsk-...",
)
# Store the API key in session state for use across pages
st.session_state.api_key = api_key

# If no API key is entered, prompt the user and stop execution
if not st.session_state.api_key:
    st.write('## Please Enter An API Key To Begin')
    st.sidebar.warning("Please Enter a key")
    st.stop()

# Create Groq client using the provided API key
client = Groq(api_key=st.session_state.api_key)

# Validate the API key by making a test request
try:
    _ = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "ping"}]
    )
except Exception as e:
    st.sidebar.warning('Invalid API Key')
    st.stop()

# Patch the Groq client with instructor for schema support (not used here, but available)
instructor_client = instructor.patch(client)

# =========================Starting Main Code===========================================#

# Sidebar: System prompt and personality selection
prompt = st.sidebar.title('System Prompt: ')

# Select the bot's personality/mode
mode = st.sidebar.selectbox(
    'Choose a Mode', ['Concise', 'Detailed', 'Normal', 'Formal', 'Vintage']
)

# Set the system prompt/personality based on selected mode
if mode == 'Normal':
    personality = 'You are a normal bot with answers that are of medium lenght and provide just enough detail that can satisfy everyone'
if mode == 'Detailed':
    personality = 'You provide detailed answers and occasionally over-explain. You also add a fun fact near the end of every response which should be related to the user\'s question and your responses are atleast 500 characters'
if mode == 'Concise':
    personality = 'You provide very little details and always sum up the key points. your answers are brief and don\'t exceed 180 characters.'
if mode == 'Formal':
    personality = 'You provide very formal answers with NO slang and use a very respectful and formal tone. You excell in formal writings such as letters.'
if mode == 'Vintage':
    personality = "You are a vintage style assistant. You speak in a polite, slightly formal tone and use old, archaic english. Use words like 'thee', 'thou', 'thy', etc. You should keep answers understandable enough for modern readers and have answers about one paragraph "

# Create Groq client for chat (redundant, but keeps code clear)
client = Groq(api_key=api_key)

# Main UI for General Chat page
st.title('Chat Bot')
st.write('### Used For Everyday Chats')

# Initialize per-page history for General Chat
if 'history_general' not in st.session_state:
    st.session_state.history_general = []
history = st.session_state.history_general

# Input box for user query and submit button
user_input = st.text_input('Enter Your Query: ', '')
if st.button('Submit'):
    # Send user query and system prompt to Groq chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role' : 'system',
                'content' : personality,
            },
            {
                'role' : 'user',
                'content' : user_input,
            }
        ],
        model='llama-3.3-70b-versatile'
    )
    # Store response in history
    response =chat_completion.choices[0].message.content
    history.append( { "query": user_input, "response" : response})
    st.write('---')
    st.markdown(f'<div class"response-box">{response}</div>', unsafe_allow_html=True)
    st.write('---')

# Sidebar: Display chat history and allow clearing
st.sidebar.title('History')
for i, entry in enumerate(history, start=1):
    if st.sidebar.button(f'Query {i}: {entry["query"]}'):
        st.write('---')
        st.markdown(f'<div class"response-box">{entry["response"]}</div>', unsafe_allow_html=True)
        st.write('---')

st.sidebar.write('---')
if st.sidebar.button('Clear History'):
    st.session_state.history_general = []