import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
import dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import model


# Load environment variables
dotenv.load_dotenv()

gemini_api_key = st.secrets["GOOGLE_API_KEY"]
if gemini_api_key is None:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=gemini_api_key)

# Functions for PDF processing and question answering
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    return text_splitter.split_text(raw_text)

def get_vector(chunks):
    if not chunks:
        return None
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", api_key=gemini_api_key)
    return FAISS.from_texts(texts=chunks, embedding=embeddings)

def user_question(question, db, chain, raw_text):
    if db is None:
        return "Please upload and process a PDF first."

    docs = db.similarity_search(question, k=5)
    response = chain.invoke(
        {"input_documents": docs, "question": question, "context": raw_text},
        return_only_outputs=True
    )
    return response.get("output_text")

def conversation_chain():
    template = """
    Answer the question in 3000 words in detail. Demonstrate it with diagrams using lines
    Context: \n{context}\n
    Question: \n{question}\n
    Answer:
    """
    model_instance = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=gemini_api_key)
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    return load_qa_chain(model_instance, chain_type="stuff", prompt=prompt), model_instance

def main():
    # Set the page configuration
    st.set_page_config(page_title="Solver", page_icon="🍵", layout="wide")
    st.header("Solver 🍵")

    # Initialize session state variables specific to this page
    if "messages_chatbot_2" not in st.session_state:
        st.session_state.messages_chatbot_2 = []
    if "vector_store_chatbot_2" not in st.session_state:
        st.session_state.vector_store_chatbot_2 = None
    if "chain_chatbot_2" not in st.session_state:
        st.session_state.chain_chatbot_2 = None
    if "raw_text_chatbot_2" not in st.session_state:
        st.session_state.raw_text_chatbot_2 = None

    # Sidebar for PDF file upload and processing
    
    pdf_docs = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")

    if st.button("Process PDF"):
        if not pdf_docs:
            st.error("Please upload at least one PDF file.")
        else:
            with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    chunks = get_text_chunks(raw_text)
                    vector_store = get_vector(chunks)
                    chain, _ = conversation_chain()

                    if vector_store and chain and raw_text:
                        st.session_state.vector_store_chatbot_2 = vector_store
                        st.session_state.chain_chatbot_2 = chain
                        st.session_state.raw_text_chatbot_2 = raw_text
                        st.success("PDF processed successfully.")

                            # Initial question for disease identification
                        initial_question = """
                            Your task is to answer the question demonstrate it with diagram using lines
                            """
                        initial_response = user_question(initial_question, vector_store, chain, raw_text)
                        st.write(f"{initial_response}")


if __name__ == "__main__":
    main()