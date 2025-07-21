import re
import os
from openai import OpenAI
from dotenv import load_dotenv
from prompts import *

from openai import OpenAI
import os
from dotenv import load_dotenv

# Initialize OpenRouter client (MODIFIED)
load_dotenv()
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    default_headers={  # Add headers here instead
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "TalentScout Hiring Assistant"
    }
)

def process_greeting_response(user_input, session_state):
    """Process the initial greeting response and collect name"""
    session_state.candidate_info["name"] = user_input.strip()
    session_state.current_state = "collect_info"
    return get_info_prompt("email", "email address")

def process_info_collection(user_input, session_state):
    """Process and validate candidate information"""
    fields_order = ["email", "phone", "experience", "position", "location"]
    
    for field in fields_order:
        if session_state.candidate_info[field] is None:
            # Validate input
            validation_msg = validate_field(field, user_input)
            if validation_msg:
                return validation_msg
            
            # Store valid input
            session_state.candidate_info[field] = user_input.strip()
            
            # Get next field or move to tech stack
            next_field = get_next_field(fields_order, field, session_state)
            if next_field:
                return get_info_prompt(next_field, next_field.replace("_", " "))
            else:
                session_state.current_state = "tech_stack"
                return get_tech_stack_prompt()
    
    return "Unexpected error in information collection."

def validate_field(field, value):
    """Validate individual fields"""
    if field == "email" and not validate_email(value):
        return "That doesn't look like a valid email address. Please try again."
    elif field == "phone" and not validate_phone(value):
        return "Please enter a valid phone number (e.g., +1234567890 or 123-456-7890)."
    elif field == "experience" and not value.isdigit():
        return "Please enter your years of experience as a number (e.g., 3)."
    return None

def get_next_field(fields_order, current_field, session_state):
    """Get the next field that needs to be collected"""
    return next(
        (f for f in fields_order[fields_order.index(current_field)+1:] 
         if session_state.candidate_info[f] is None),
        None
    )

def process_tech_stack(user_input, session_state):
    """Process tech stack input and generate questions"""
    session_state.candidate_info["tech_stack"] = user_input.strip()
    session_state.current_state = "technical_questions"
    
    # Generate technical questions
    tech_questions = generate_llm_response(
        generate_technical_questions(user_input),
        temperature=0.7,
        max_tokens=500
    )
    
    # Store and format questions
    questions = [q.strip() for q in tech_questions.split("\n") if q.strip()]
    session_state.candidate_info["technical_questions"] = questions
    
    return (
        f"Great! Let's assess your technical skills.\n\n{questions[0]}" 
        if questions 
        else "Let me prepare some technical questions for you..."
    )

def process_tech_stack(user_input, session_state):
    session_state.candidate_info["tech_stack"] = user_input.strip()
    session_state.current_state = "technical_questions"
    
    # Generate exactly 3 technical questions
    prompt = f"""Generate exactly 3 technical interview questions about {user_input}. 
    Each question should:
    - Be a single complete sentence
    - Start with "What", "How", or "Explain"
    - Focus on practical application
    - Be separated by newlines
    Example:
    How would you optimize memory usage in a Python application?
    What are the key differences between lists and tuples?
    Explain how you would implement authentication in a web application?"""
    
    tech_questions = generate_llm_response(prompt, temperature=0.7, max_tokens=300)
    
    # Extract exactly 3 clean questions
    questions = [q.strip() for q in tech_questions.split('\n') 
                if q.strip() and q.strip()[0].isupper()][:3]
    
    # Fallback if generation fails
    if len(questions) < 3:
        questions = [
            f"What's the most challenging {user_input} problem you've solved?",
            f"How would you debug performance issues in {user_input}?",
            f"Explain an advanced concept in {user_input}"
        ]
    
    session_state.candidate_info["technical_questions"] = questions
    session_state.current_question_index = 0  # Track which question we're on
    
    return f"Let's begin with question 1/3:\n\n{questions[0]}"

def process_technical_questions(user_input, session_state):
    questions = session_state.candidate_info["technical_questions"]
    current_idx = session_state.current_question_index
    
    # Evaluate answer
    evaluation = generate_llm_response(
        f"Evaluate this answer to '{questions[current_idx]}': {user_input}",
        temperature=0.3,
        max_tokens=200
    )
    
    # Move to next question or finish
    session_state.current_question_index += 1
    
    if session_state.current_question_index < len(questions):
        return (f"Evaluation: {evaluation}\n\n"
               f"Question {session_state.current_question_index + 1}/3:\n\n"
               f"{questions[session_state.current_question_index]}")
    else:
        session_state.current_state = "complete"
        return (f"Evaluation: {evaluation}\n\n"
               "You've completed all technical questions!\n"
               f"{get_farewell()}")

def get_current_question_index(messages, questions):
    """Get index of current question being answered"""
    return len([m for m in messages 
               if m["role"] == "assistant" and 
               any(q in m["content"] for q in questions)])

def evaluate_answer(question, answer, current_q_index, questions):
    """Evaluate candidate's answer to technical question"""
    return generate_llm_response(
        evaluate_technical_response(question, answer),
        temperature=0.3,
        max_tokens=300
    )

def format_next_question(evaluation, next_question):
    """Format evaluation with next question"""
    return f"{evaluation}\n\nNext question:\n\n{next_question}"

def validate_email(email):
    """Validate email format"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    """Validate phone number format"""
    patterns = [
        r"^(\+\d{1,3}[- ]?)?\d{10}$",
        r"^\d{3}[- ]?\d{3}[- ]?\d{4}$"
    ]
    return any(re.match(pattern, phone) for pattern in patterns)

def generate_llm_response(prompt, temperature=0.5, max_tokens=300):
    """Generate response using OpenRouter API"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a professional hiring assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
           
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating LLM response: {e}")
        return "I'm having trouble generating a response. Please try again later."

def handle_unknown_input(user_input):
    """Handle unrecognized user input"""
    return "I'm not sure how to respond to that. Could you please rephrase or say 'exit' if you'd like to end the conversation?"