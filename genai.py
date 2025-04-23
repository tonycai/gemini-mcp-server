import google.generativeai as genai
import os

# Configure the API key (replace with your actual API key)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("Error: Please set the GOOGLE_API_KEY environment variable.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

    # Load the Gemini 2.5 Pro Preview model
    model = genai.GenerativeModel('gemini-2.5-pro-preview-03-25')

    # Your prompt
    prompt = "Explain the basics of quantum physics in simple terms."

    try:
        # Generate the response
        response = model.generate_content(prompt)
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")