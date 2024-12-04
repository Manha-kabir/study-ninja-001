import streamlit as st
import model

# Set the page configuration
st.set_page_config(page_title="Tutor 🧑‍🏫", page_icon="🧑‍🏫", layout="wide")
st.header("Tutor 🧑‍🏫")

# Retrieve content from session state
content = st.session_state.get('content', '')

# Initialize chat history specific to this page
if "messages_chatbot_1" not in st.session_state:
    st.session_state.messages_chatbot_1 = []

# Display chat messages from history on app rerun
for message in st.session_state.messages_chatbot_1:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Warning if no content is uploaded
if content == "":
    st.warning("For more accurate doubt solving, upload your notes")

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages_chatbot_1.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using the model
    model_response = model.model(prompt, history=st.session_state.messages_chatbot_1, context=content)
    
    # Add assistant response to chat history
    st.session_state.messages_chatbot_1.append({"role": "assistant", "content": model_response})
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(model_response)
