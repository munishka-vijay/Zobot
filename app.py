# app.py
import os
import streamlit as st
import openai
from configparser import ConfigParser

def load_env():
    config = ConfigParser()
    config.optionxform = str  # Preserve case sensitivity
    with open(".env", "r") as f:
        config.read_string("[environment]\n" + f.read())  # Add a section header to the file contents
    for key, value in config.items("environment"):
        os.environ[key] = value

# loading the evironment variables
load_env()
# Get the API key from environment variable
api_key = os.environ.get("OPENAI_API_KEY")

st.set_page_config(page_title="Zobot", page_icon=":robot_face:")

def get_gpt_response(prompt, model="gpt-4o"):
    """ Function to get a response from GPT-4o """
    openai.api_key = api_key
    # Retrieve conversation history from session state
    conversation_history = st.session_state.get('conversation', [])
    # Add the user's prompt to the conversation history
    conversation_history.append(("user", prompt))
    # Generate response from GPT-4o
    response = openai.chat.completions.create(
          model=model,
          messages=[{"role": role, "content": message} for role, message in conversation_history],
          max_tokens=1000,
          temperature=0.7,
          n=1,
          stop=None
      )
    # Extract and return the response
    chatbot_response = response.choices[0].message.content
    # Add chatbot response to the conversation history
    conversation_history.append(("assistant", chatbot_response))  # Assuming the chatbot response has the role of 'assistant'
    # Update conversation history in session state
    st.session_state['conversation'] = conversation_history
    return chatbot_response

# Streamlit application UI
st.title("Zobot - Your Foodie Friend")

# Chat input box
user_input = st.text_input("You: ", "")

# Store conversation history in session state
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

if user_input:
    # Get the response from the chatbot
    response = get_gpt_response(user_input)
    # Display the chatbot's response
    st.write("Zobot:", response)

if __name__ == "__main__":
    pass
