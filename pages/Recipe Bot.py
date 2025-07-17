# Recipe Bot page
# Handles recipe generation, schema validation, and per-page history
import streamlit as st
from groq import Groq
import instructor
from pydantic import BaseModel, Field
from typing import List

# Set up the Streamlit page configuration
st.set_page_config(
    page_title='Recipe Bot',
    page_icon=':material/chef_hat:'
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

# Patch the Groq client with instructor for schema support
instructor_client = instructor.patch(client)

# ======================================Starting Main Code======================================================

# Main UI for Recipe Bot page
st.title("Recipe Bot")
st.write('### Used For Finding Desired Recipes')

# Initialize per-page history for Recipe Bot
if 'history_recipe' not in st.session_state:
    st.session_state.history_recipe = []
history = st.session_state.history_recipe

# Pydantic schema for recipe ingredients and recipe
class RecipeIngredient(BaseModel):
    name: str
    quantity: str
    unit: str = Field(description="The unit of measurement, like cup, tablespoon, etc.")

class Recipe(BaseModel):
    title: str
    description: str
    prep_time_minutes: int
    cook_time_minutes: int
    ingredients: List[RecipeIngredient]
    instructions: List[str]

# Function to get a recipe from Groq using the instructor client
def recipe_get(recipe_name):
    return instructor_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=Recipe,
        messages=[
            {"role": "user", "content": f"Give me a recipe for {recipe_name}"}
        ]
    )

# Input box for recipe name and button to fetch recipe
recipe_input = st.text_input("Enter the Name of Your Recipe:")
if st.button("Enter"):
    try:
        # Get recipe from Groq API
        recipe = recipe_get(recipe_input)
        st.header(recipe.title)
        st.write(recipe.description)
        st.write(f"Prep time: {recipe.prep_time_minutes} min")
        st.write(f"Cook time: {recipe.cook_time_minutes} min")

        st.subheader("Ingredients")
        for ing in recipe.ingredients:
            st.write(f"- {ing.quantity} {ing.unit} {ing.name}")

        st.subheader("Instructions")
        for i, step in enumerate(recipe.instructions, 1):
            st.write(f"{i}. {step}")

        # Store recipe in history
        history.append({'query': recipe_input, 'response': recipe})

    except Exception as e:
        st.error(f"Error: {e}")

# Sidebar: Display recipe history and allow clearing
st.sidebar.title("History")
for i, entry in enumerate(history, start=1):
    if st.sidebar.button(f'{i}: {entry["query"]}'):
        recipe = entry["response"]
        st.header(recipe.title)
        st.write(recipe.description)
        st.write(f"Prep time: {recipe.prep_time_minutes} min")
        st.write(f"Cook time: {recipe.cook_time_minutes} min")
        st.subheader("Ingredients")
        for ing in recipe.ingredients:
            st.write(f"- {ing.quantity} {ing.unit} {ing.name}")
        st.subheader("Instructions")
        for i, step in enumerate(recipe.instructions, 1):
            st.write(f"{i}. {step}")

st.sidebar.write('---')
if st.sidebar.button("Clear History"):
    st.session_state.history_recipe = []