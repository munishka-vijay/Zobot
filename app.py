"""
Contains code to run chatbot
"""

import os
import pandas as pd
from configparser import ConfigParser
import streamlit as st
import openai

def load_env():
    """
    Function to load env variables
    """
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

# Function to get a response from GPT-4o using the chat/completions endpoint
def get_gpt_response(prompt, model="gpt-4o"):
    """ Function to get a response from GPT-4o """
    openai.api_key = api_key
    
    # Retrieve conversation history from session state
    conversation_history = st.session_state.get('conversation', [])
    
    # Add the user's prompt to the conversation history
    conversation_history.append({"role": "user", "content": prompt})
    
    # Generate response from GPT-4o
    response = openai.chat.completions.create(
        model=model,
        messages=conversation_history,
        max_tokens=1000,
        temperature=0.7,
        n=1,
        stop=None
    )
    
    # Extract and return the response
    chatbot_response = response.choices[0].message.content
    
    # Add chatbot response to the conversation history with the role "assistant"
    conversation_history.append({"role": "assistant", "content": chatbot_response})
    
    # Update conversation history in session state
    st.session_state['conversation'] = conversation_history
    return chatbot_response

# Function to load initial prompt from a text file
def load_initial_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Function to load data from a CSV file
def load_csv_data(file_path):
    return pd.read_csv(file_path)

# Streamlit application UI
st.title("Zobot - Your Foodie Friend")

# Load initial prompt
initial_prompt = load_initial_prompt('initial_prompt.txt')

# Load data from CSV
data = load_csv_data('training_data.csv')

# Initialize conversation history in session state with the initial prompt
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = [{"role": "assistant", "content": initial_prompt}]
    # Optionally, you can also store the data in session state if needed later
    st.session_state['data'] = data

# Chat input box
user_input = st.chat_input("You: ")

if user_input:
    # Get the response from the chatbot
    response = get_gpt_response(user_input)


# Display conversation history in order, including the latest response at the bottom
for message in st.session_state['conversation'][1:]:  # Skip the first message
    speaker = "You" if message['role'] == "user" else "Zobot"
    st.markdown(f"**{speaker}:** {message['content']}")


if __name__ == "__main__":
    pass