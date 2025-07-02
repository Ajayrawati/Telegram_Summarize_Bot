import os
from dotenv import load_dotenv
import google.generativeai as genai


# Function to summarize the transcript using generative AI
def summarize_text(user_input):
    load_dotenv()  # Load environment variables from .env file

    # Access the API key
    api_key = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=api_key)  # Configure the generative AI API
    model = genai.GenerativeModel('gemini-1.5-flash')  # Initialize the model

    # Define the pre-prompt (system instruction)
    pre_prompt = """
    Summarize the following content into  concise bullet points:
    Don't use ** for higlight or any thing you can use emoji and icon do this instead remember this before generating text
    also not for heading or anything remove * FROM everything.
    """
    full_prompt = f"{pre_prompt}\n\nUser: {user_input}"

    response = model.generate_content(full_prompt)

    return response.text

