import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import time 

class ATSResume():
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        # st.subheader("Smart ATS")
        # st.text("Improve Your Resume ATS")
        st.session_state.waiting = True  

    def get_gemini_response(self,user_query):
        model = genai.GenerativeModel(model_name="gemini-pro")
        response = model.generate_content(user_query)
        return response.text
    
    def input_pdf_text(self,uploaded_file):
        reader = pdf.PdfReader(uploaded_file)
        text=""
        for page in range(len(reader.pages)):
            page=reader.pages[page]
            text+=str(page.extract_text())
        return text
    
    def get_template(self)->str:
        template="""
        Hey Act Like a skilled or very experience ATS(Application Tracking System)
        with a deep understanding of tech field,software engineering,data science ,data analyst
        and big data engineer. Your task is to evaluate the resume based on the given job description.
        You must consider the job market is very competitive and you should provide 
        best assistance for improving thr resumes. Assign the percentage Matching based 
        on Jd and
        the missing keywords with high accuracy, also provide the improvements needed in the resume for better JD Match.
        resume:{text}
        description:{jd}

        I want the response in one single string having the structure
        {{\n
        "JD Match":"%",\n
        "MissingKeywords":[]",\n
        "Profile Summary":"",\n
        "Improvement":""\n
        }}
        """
        return template
    
    def resume(self,job_description_query,uploaded_file):
        jd= job_description_query
        # uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")
        # submit = st.button("Submit")
        # if uploaded_file is not None:
        text= self.input_pdf_text(uploaded_file)
        response= self.get_gemini_response(self.get_template())
        return response
                