import streamlit as st
import fitz  # PyMuPDF
import io

# Function to extract text from PDF file
def extract_pdf_content(pdf_file):
    # Open the PDF file using PyMuPDF from byte stream
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    
    # Iterate through each page and extract text
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()  # Get text from each page
    
    return text

# Check if the user has uploaded a PDF


def main():
    st.set_page_config(page_title="Study Ninja - Lets You Focus 🥷", page_icon="🥷", layout="wide")
    
    
    st.write('## 😃 Welcome to Study Ninja 🥷. Lets get started ')
    uploaded_file = st.file_uploader("Upload your Notes here (Only PDF's)", type="pdf")

    if uploaded_file is not None:
    # Extract the text content from the uploaded PDF
        content = extract_pdf_content(uploaded_file)
    
    # Save the extracted content to session_state for persistence
        st.session_state['content'] = content
    
    # Inform the user that the file was processed
        st.success("PDF content successfully extracted.")
        st.query_params.from_dict({"page": "notes"})  
    else:
        st.warning("Uploded the notes so we can start learning")
        
    st.write("### After Done Comeback and clear this session so we can perform more efficiently")   
    if st.button("Clear Session"):
        st.session_state.clear()
        st.query_params.clear() 
    
if __name__ == "__main__":
    main()    
