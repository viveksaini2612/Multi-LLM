from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

import os
import anthropic
import google.generativeai as genai

# Load API keys
claude_api_key = os.getenv("MY_ANTHROPIC_KEY")
gemini_api_key = os.getenv("MY_GEMINI_KEY")

# Setup Claude client
claude_client = anthropic.Anthropic(api_key=claude_api_key)

# Setup Gemini client
genai.configure(api_key=gemini_api_key)

claude_model_name = "claude-3-opus-20240229"
gemini_model_name = "models/gemini-2.5-flash-preview-04-17"

# --- Claude ---
def call_claude(prompt):
    try:
        response = claude_client.messages.create(
            model=claude_model_name,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        return f"Error calling Claude: {str(e)}"

# --- Gemini ---
def call_gemini(prompt):
    try:
        model = genai.GenerativeModel(model_name=gemini_model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini: {str(e)}"

# --- Model Router ---
def choose_model(prompt):
    """
    Refined routing logic:
    - If the prompt contains math-related terms (e.g., multiply, plus, equation), send to Claude.
    - Otherwise, use Gemini for general or creative tasks.
    """
    prompt_lower = prompt.lower()
    math_keywords = ["math", "multiply", "addition", "subtraction", "divide", "solve", "equation", "calculation"]
    
    if any(kw in prompt_lower for kw in math_keywords):
        return "claude"
    return "gemini"


def get_response(prompt):
    model = choose_model(prompt)
    print(f"\nUsing {model.capitalize()} for this request...")
    if model == "claude":
        return call_claude(prompt)
    return call_gemini(prompt)

# --- Entry point ---
if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    response = get_response(prompt)
    print("\nResponse:\n", response)
