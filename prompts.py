def get_greeting():
    return """Hello! I'm TalentScout's AI Hiring Assistant. 
I'll help with the initial screening process by collecting some basic information and asking relevant technical questions.

Could you please start by telling me your full name?"""

def get_farewell():
    return """Thank you for your time! Your information has been recorded and our team will review your responses.

We'll be in touch soon regarding next steps in the hiring process. Have a great day!"""

def get_info_prompt(field_name, field_description):
    prompts = {
        "email": "Could you please share your email address?",
        "phone": "What's the best phone number to reach you?",
        "experience": "How many years of professional experience do you have?",
        "position": "What position are you applying for?",
        "location": "Where are you currently located (city/country)?",
    }
    return prompts.get(field_name, f"Could you please provide your {field_description}?")

def get_tech_stack_prompt():
    return """Please list the technologies in your tech stack (programming languages, frameworks, databases, tools).
    
For example: Python, JavaScript, React, PostgreSQL, Docker"""

def generate_technical_questions(tech_stack):
    prompt = f"""Generate 3-5 technical questions to assess a candidate's proficiency in the following technologies:
{tech_stack}

For each technology, provide questions that cover:
- Fundamental concepts
- Practical application
- Problem-solving

Format the questions clearly and make them relevant to a professional setting."""

    return prompt

def evaluate_technical_response(question, answer):
    return f"""Evaluate the following technical question and answer:

Question: {question}
Answer: {answer}

Provide:
1. A brief assessment of the answer's accuracy (0-10 scale)
2. Key points the answer should have covered
3. Any improvements or additional details the candidate could provide

Keep the evaluation professional and constructive."""