from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from new_referral import Referral
from ats_resume import ATSResume
import streamlit as st

class EmployeeHRChat:
    def __init__(self):
        """Initialize the HR Onboarding Assistant with fixed model and prompt template."""
        self.llm = ChatOllama(model="mistral")
        self.prompt = self.create_prompt()
        self.chain = self.create_chain(self.prompt, self.llm)
        self.new_referral = Referral()
        self.ats_resume = ATSResume()
    def create_prompt(self):
        template = """
        You are a helpful and knowledgeable HR Assistant.
        Your job is to assist employees with their queries by answering their questions, providing information, and guiding them through various tasks.
        You should always be friendly, professional, and precise in your responses.

        Consider the following chat history to understand the context of the conversation:
        Chat history: {chat_history}

        User question: {user_question}

        Your response should address the user’s question while maintaining a helpful and positive tone.
        """
        return ChatPromptTemplate.from_template(template=template)

    def create_chain(self, prompt, llm):
        return prompt | llm | StrOutputParser()

    def invoke_chain(self, chat_history: str, user_question: str):
        return self.chain.invoke({
            "chat_history": chat_history,
            "user_question": user_question
        })
    
    def process_referral_details(self, context):
        try:
            extracted_data, formatted_output = self.new_referral.extract_details(context)
            return formatted_output
        except Exception as e:
            print(f"Error generating response process hire details: {e}")

    def handle_user_query(self, chat_history, user_query,uploaded_file=False):
        if uploaded_file is not False:
            with st.spinner("Generating..."):
                uploaded_file = st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")
            ats_score = self.ats_resume.resume(job_description_query=user_query,uploaded_file=uploaded_file)
            return ats_score
        template = self.new_referral.details_template()
        print("CHAT HISTORY:",st.session_state.chat_history[-1].content)
        if st.session_state.chat_history[-2].content == template:
            return self.process_referral_details(user_query)
        if user_query.lower()=='referral':
            return template
        elif user_query.lower()=='resume':
                return "Please provide resume and job description."
        else:
            return self.invoke_chain(chat_history, user_query)