
# LLM Integration Via Groq


This project is a functioning chat bot via _groq_.

It provides:
- A **Home page**.
- A **General Chat Bot** for freeform conversations with different personality modes.
- A **Recipe Bot** for generating structured recipes.

## Features

**Secure API Key Input**  
- Enter your GROQ API key — it’s stored in session state for use across all pages.

**API Key Validation**  
- The app checks your key by making a test request using _ping_.

**General Chat Bot**  
- Choose your chat bot’s **personality**:  
  - Normal: Balanced, everyday tone.  
  - Detailed: In-depth explanations with fun facts.  
  - Concise: Short, summarized answers.  
  - Formal: Professional and polished replies.  
  - Vintage: Old-style English with a charming archaic tone.
- Maintains **per-page chat history** that you can review and clear.

**Recipe Bot**  
- Enter a dish name and get:
  - Title
  - Description
  - Prep & cook time
  - Structured ingredients list
  - Step-by-step instructions
- Uses **Pydantic schema** validation with `instructor` for structured data.
- Maintains **recipe query history** for easy reloading.

---

##  How It Works

###  Home Page

- Prompts for your GROQ API key.
- Gives an error message if the key is incorrect
- Prevents access to other pages without a valid key.

###  General Chat Bot

- Select a personality mode from the sidebar.
- Enter your question ? Get a customized response.
- View or clear chat history from the sidebar.

### Recipe Bot

- Enter a recipe name.
- Fetches a structured recipe using `instructor` for response parsing.
- Displays the recipe with clear sections for ingredients and instructions.
- View or clear your recipe history.

---

## Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- [streamlit](https://docs.streamlit.io/)
- [groq](https://groq.dev/)
- [instructor](https://pypi.org/project/instructor/)
- [pydantic](https://docs.pydantic.dev/)

Install everything with:

```bash
pip install streamlit groq instructor pydantic
```

## How to Run

- After installing the necessary packages, open your desired terminal and type `cd _filepath_`. 
- Then type `streamlit run Home.py`
- It will then automatically redirect you to the web app and will also display a network port which can let anyone on the network access it.
