import streamlit as st
import os
import google.generativeai as genai

# Check if there is content in session_state
content = st.session_state.get('content', '')

# Retrieve the API key from Streamlit secrets
gemini_api_key = st.secrets["GOOGLE_API_KEY"]

# Function to format text using Google Generative AI
def format_text(text):
    # Configuration for the generation model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Create the generative model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "Format the given text into a human-understandable way. "
            "No need to explain anything. Remember that we are using Streamlit 'markdown' "
            "feature to show the content extracted from the PDF."
        ),
    )

    # Start a chat session with the model
    chat_session = model.start_chat(history=[])

    # Send the text to be formatted to the model
    response = chat_session.send_message(f"text to be formatted: {text}")

    # Return the formatted text from the response
    return response.text

# Main function to display the formatted content in Streamlit
def main():
    formated_content = format_text(content)
    if content:
        # Display the formatted content extracted from the PDF
        st.markdown(formated_content)
    else:
        # Display a warning if no content is found
        st.warning("Didn't receive your notes yet 😒")

# Run the Streamlit app
if __name__ == "__main__":
    st.set_page_config(page_title="Notes 📝", page_icon="📒", layout="wide")
    st.header("Notes 📝")
    main()
