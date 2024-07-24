from transformers import pipeline
from langchain_core.prompts import PromptTemplate
import os
import pandas as pd
import streamlit as st

class Referral:
    def __init__(self):
        self.llm = pipeline(task="question-answering",model="twmkn9/albert-base-v2-squad2")
        self.queries = {
            "applicant_name": "What is the applicant's name?",
            "role": "What role is the applicant applying for?",
            "city_type": "Does the applicant live in an metro or non area?",
            "previous_ctc": "What was the applicant's previous CTC?",
            "previous_job_switches": "How many times has the applicant switched jobs?",
            "graduation_marks": "What were the applicant's graduation marks?",
            "previous_exp": "How many months of previous experience does the applicant have?",
            "expected_ctc": "What is the applicant's expected CTC?"
        }
    
    def get_answers(self,context):
        try:
            queries = self.queries
            answers = {}
            for key, question in queries.items():
                result = self.llm(question=question,context=context)
                answers[key] = result['answer']
            return answers
        except Exception as e:
            print(f"Error generating response get answers: {e}")

    def details_template(self):
        template = """
            Please provide the applicant's details for further processing.\n\n
            "Name": \n
            "Role": \n
            "City type": \n
            "Previous CTC": \n
            "Previous job changes": \n
            "Graduation marks": \n
            "Exp (Months)": \n
            "CTC": \n
            """
        return template
    
    def extract_details(self,user_query):
        try:
            extracted_data = self.get_answers(context=user_query)
            template = """
            Based on the provided context we get following details:\n\n
            {{\n
                "Name": {applicant_name},\n
                "Role": {role},\n
                "City type": {city_type},\n
                "Previous CTC": {previous_ctc},\n
                "Previous job changes": {previous_job_switches},\n
                "Graduation marks": {graduation_marks},\n
                "Exp (Months)": {previous_exp},\n
                "CTC": {expected_ctc}\n
            }} 

            """

            formatted_output = template.format(
                applicant_name=extracted_data['applicant_name'],
                role=extracted_data['role'],
                city_type=extracted_data['city_type'],
                previous_ctc=extracted_data['previous_ctc'],
                previous_job_switches=extracted_data['previous_job_switches'],
                graduation_marks=extracted_data['graduation_marks'],
                previous_exp=extracted_data['previous_exp'],
                expected_ctc=extracted_data['expected_ctc']
            )
            self.save_applicant_details(extracted_data)
            return extracted_data,formatted_output
        except Exception as e:
            print(f"Error generating response Extract Details: {e}")

    def save_applicant_details(self,applicant_details):
        existing_df = pd.DataFrame()
        data_path = './data/NewJoiners.csv'
        if os.path.exists(data_path):
            existing_df = pd.read_csv(data_path)
        updated_df = pd.concat([existing_df, pd.DataFrame([applicant_details])], ignore_index=True)
        updated_df.to_csv(data_path, index=False)
        return st.success("Applicant details saved successfully.")