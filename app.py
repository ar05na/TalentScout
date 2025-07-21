import streamlit as st
from openai import OpenAI
from prompts import *
from utils import *
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"))

# Configure Streamlit page
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")
st.title("TalentScout Hiring Assistant")
st.markdown("""
    Welcome to TalentScout's AI Hiring Assistant. I'll help with the initial screening process by:
    - Collecting your basic information
    - Asking relevant technical questions based on your skills
    - Assessing your qualifications for the role
""")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": get_greeting()}]
    st.session_state.candidate_info = {
        "name": None,
        "email": None,
        "phone": None,
        "experience": None,
        "position": None,
        "location": None,
        "tech_stack": None,
        "technical_questions": []
    }
    st.session_state.current_state = "greeting"

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your response here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check for exit keywords
    if any(exit_word in prompt.lower() for exit_word in ["exit", "quit", "goodbye", "stop"]):
        st.session_state.messages.append({"role": "assistant", "content": get_farewell()})
        with st.chat_message("assistant"):
            st.markdown(get_farewell())
        st.stop()
    
    # Process user input based on current state
    if st.session_state.current_state == "greeting":
        response = process_greeting_response(prompt, st.session_state)
    elif st.session_state.current_state == "collect_info":
        response = process_info_collection(prompt, st.session_state)
    elif st.session_state.current_state == "tech_stack":
        response = process_tech_stack(prompt, st.session_state)
    elif st.session_state.current_state == "technical_questions":
        response = process_technical_questions(prompt, st.session_state)
    else:
        response = handle_unknown_input(prompt)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Display candidate info sidebar (for debugging/verification)
    with st.sidebar:
        st.subheader("Candidate Information")
        for key, value in st.session_state.candidate_info.items():
            if key != "technical_questions":
                st.text(f"{key.replace('_', ' ').title()}: {value or 'Not provided'}")
        
        if st.session_state.candidate_info["technical_questions"]:
            st.subheader("Technical Questions")
            for i, q in enumerate(st.session_state.candidate_info["technical_questions"], 1):
                st.text(f"Q{i}: {q}")
