import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from chat import EmployeeHRChat

class EmployeeHRAssistant:
    def __init__(self):
        st.set_page_config(page_title="HR Assistant ChatApp")
        st.title("HR Assistant ChatApp")
        self.employeehrchat = EmployeeHRChat()
        self.initialize_session()

    def initialize_session(self):
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                AIMessage(
                    content="""
                        Hello! I am a HR Assistant ChatApp. How may I help you?\n
                        1. Add new referral (use prompt: referral)
                        2. Suggesting new courses to the employee if needed.
                    """
                )
            ]
        return st.session_state.chat_history

    def handle_user_message(self, user_query):
        with st.chat_message("Human"):
            st.markdown(user_query)

        with st.chat_message("AI"):
            with st.spinner("Generating response..."):
                try:
                    print("HANDLE USER MESSAGE:",st.session_state.chat_history[-1].content)
                    if st.session_state.chat_history[-1].content=="resume":
                        response = self.employeehrchat.handle_user_query(chat_history=st.session_state.chat_history, user_query=user_query,uploaded_file=True)
                        st.write(response)
                        st.session_state.chat_history.append(AIMessage(content=response))
                    response = self.employeehrchat.handle_user_query(chat_history=st.session_state.chat_history, user_query=user_query)
                    st.write(response)
                    st.session_state.chat_history.append(AIMessage(content=response))
                except Exception as e:
                    st.error(f"Error generating response: {e}")

    def display_chat_history(self):
        for message in st.session_state.chat_history:
            if isinstance(message, AIMessage):
                with st.chat_message("AI"):
                    st.write(message.content)
            elif isinstance(message, HumanMessage):
                with st.chat_message("Human"):
                    st.write(message.content)

    def run(self):
        self.display_chat_history()
        user_query = st.chat_input("Type your message here...")
        if user_query:
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            self.handle_user_message(user_query)

if __name__ == '__main__':
    app = EmployeeHRAssistant()
    app.run()