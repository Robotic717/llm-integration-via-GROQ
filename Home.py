
# Home page for the Chat Bot App
# Handles API key input, validation, and provides navigation instructions
import streamlit as st
from groq import Groq
import instructor


# Set up the Streamlit page configuration
st.set_page_config(
    page_title='Home',
    page_icon=':material/home:'
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


# Patch the Groq client with instructor for schema support (not used on Home page, but available)
instructor_client = instructor.patch(client)


# Main UI for Home page
st.title('Welcome To My Chat Bot App')
st.write('### Select a page from the sidebar')