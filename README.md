# TalentScout
# AI Hiring Assistant Chatbot

## Overview
An intelligent chatbot that automates technical candidate screening by:
- Collecting candidate information
- Generating personalized technical questions
- Evaluating responses using AI
- Providing structured feedback

## Installation

### Requirements
- Python 3.9 or later
- OpenRouter API key (free tier available)

### Setup
1. **Clone the repository**:
git clone https://github.com/ar05na/TalentScout.git

2. **Create virtual environment**:
   `python -m venv venv`
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

3. **Install dependencies**:
`pip install -r requirements.txt`


4. **Configure API key**:
Create a `.env` file with:
OPENROUTER_API_KEY=`your_api_key_here`

## Usage
Start the application:

`streamlit run app.py`



### Interview Flow
1. **Information Collection**:
   - Contact details
   - Experience level
   - Technical skills

2. **Technical Assessment**:
   - 3 adaptive technical questions
   - Real-time answer evaluation

3. **Completion**:
   - Summary report
   - Next steps

## Technical Details

### System Architecture
- **Frontend**: Streamlit
- **Backend**: OpenRouter AI
- **Core Language**: Python 3.9

### Models Used
- Primary Model: `openai/gpt-3.5-turbo`
- Parameters:
  - Temperature: 0.7 (questions), 0.3 (evaluations)
  - Max tokens: 400
  - Timeout: 30 seconds
### Prompt Design <a name="prompt-design"></a>
**1. Information Gathering Prompts**
Engineered to extract specific candidate details while maintaining natural conversation flow:
Collect {field} from candidate with:
1. Clear instructions (e.g., "Please share your {field}")
2. Format examples (e.g., "Example: {example}")
3. Validation rules (regex patterns for email/phone)
4. Error messages for invalid inputs

**2. Technical Question Generation**
Three-tiered approach for balanced assessments:

Generate {position}-specific questions about {tech_stack}:
1. Fundamental Concept:
   "Explain {core_technology} architecture"

2. Practical Application:
   "How would you {real_world_scenario}"

3. Problem-Solving:
   "Debug this {error_scenario}"

### Key Design Principles:

**Context Retention**: Each prompt references previous answers

**Difficulty Scaling**: Questions adapt to years of experience

**Anti-Bias**: Neutral phrasing without leading language

**GDPR Compliance**: No sensitive data retention in prompts

### Challenges & Solutions <a name="challenges-solutions"></a>
Challenge	Solution	Implementation
Inconsistent API Responses	Strict output formatting + validation	Added regex validation to prompts
Conversation Context Loss	State machine architecture	Streamlit session_state tracking
Technical Question Quality	Three-tier validation system:
- **Model-level constraints**
- **Post-generation filtering**
- **Fallback questions**
  
Candidate Experience Gaps	Dynamic difficulty adjustment	Experience-based prompt modification
Data Privacy Concerns	Ephemeral session storage	No database persistence

#### OpenRouter Header Requirements

Problem: Standard OpenAI client rejected custom headers

Fix: Created custom API wrapper with requests library

#### Question Relevance

Problem: Generic questions for niche technologies

Solution: Added technology-specific examples to prompts




