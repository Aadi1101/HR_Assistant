import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import markdown
import pdfkit
from io import BytesIO

# Initialize the LLM
llm = Ollama(model="mistral")

# Define the prompt template
template = """
You are an expert Business Analyst in every field, your task is to provide the technical and non-technical requirements based on the {project_description}. Additionally, you have to provide the team required with skills and designation to complete the project and estimated cost of the project in Indian Rupees. Firstly, provide a summary of the project, followed by technical and non-technical requirements, then the team details, and finally the estimated cost of the project in Indian Rupees.
"""
prompt = PromptTemplate.from_template(template=template)

# Define the processing chain
chain = prompt | llm | StrOutputParser()

# Function to generate PDF from markdown text
def generate_pdf(text):
    html_content = markdown.markdown(text)
    pdf = pdfkit.from_string(html_content, False)
    return pdf

# Streamlit app configuration
st.set_page_config(page_title="Business Requirement Analysis")
st.header("Business Requirement Document App")

# Input for project description
project_description = st.text_input("Input: ", key="input")
submit1 = st.button("Ask the Question")

# Process the input and generate response
if submit1:
    response = chain.invoke({"project_description": project_description})
    st.subheader("The Response is being generated...")
    st.write(response)
    
    # Generate and provide PDF for download
    # pdf_data = generate_pdf(response)
    # st.download_button(
    #     label="Download PDF",
    #     data=pdf_data,
    #     file_name='business_requirements.pdf',
    #     mime='application/pdf'
    # )
