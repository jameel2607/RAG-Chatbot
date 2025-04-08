import streamlit as st
from api_utils import chat_with_bot

def display_chat_interface(model: str, session_id: str):
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner('Thinking...'):
                try:
                    response = chat_with_bot(
                        prompt, 
                        model,
                        session_id=session_id
                    )
                    if "429" in response or "quota" in response.lower():
                        st.warning("The API is currently rate limited. Please wait a few seconds and try again.")
                    else:
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
