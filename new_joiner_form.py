import streamlit as st
import os 
import pandas as pd
import time 
def display_new_joiner_form():
    st.subheader("Enter the new employee details...")
    ROLE = ["Manager", "Executive"]
    CITY_TYPE = ["Metro", "Non-Metro"]

    # st.session_state.user_query_counter += 1
    with st.form(f"my_form"):
        applicant_name = st.text_input(label="Applicant Name*",key="a")
        role = st.selectbox(label="Role*", options=ROLE)
        city_type = st.selectbox(label="City Type", options=CITY_TYPE)
        # st.session_state.user_query_counter += 1
        previous_ctc = st.text_input("Previous CTC*",key="b")
        previous_job_switches = st.slider("Job Switches*", 0, 15, 1)
        graduation_marks = st.slider("Graduation Marks (optional)", 60, 100, 60)
        previous_exp = st.slider("Years of Experience* (Months)", 0, 170, 5)
        # st.session_state.user_query_counter += 1
        expected_ctc = st.text_input("Expected CTC", key="c")
        st.markdown("Required*")
        submit_button = st.form_submit_button(label="Submit Applicant Details",on_click=set_application_details(applicant_name,role,city_type,previous_ctc,previous_job_switches,graduation_marks,previous_exp,expected_ctc))
    
    while applicant_name=='':
        if submit_button:
            set_application_details(applicant_name,role,city_type,previous_ctc,previous_job_switches,graduation_marks,previous_exp,expected_ctc)
            print("after submit button")
        else: time.sleep(60)

def set_application_details(applicant_name, role, city_type, previous_ctc, previous_job_switches, graduation_marks, previous_exp, expected_ctc):
    applicant_details = {
        "Name": applicant_name,
        "Role": role,
        "City type": city_type,
        "Previous CTC": previous_ctc,
        "Previous job changes": previous_job_switches,
        "Graduation marks": graduation_marks,
        "Exp (Months)": previous_exp,
        "CTC": expected_ctc
    }
    save_applicant_details(applicant_details)

def save_applicant_details(applicant_details):
        # applicant_details = st.session_state.applicant_details

    if applicant_details:
        existing_df = pd.DataFrame()
        data_path = './data/NewJoiners.csv'
        if os.path.exists(data_path):
            existing_df = pd.read_csv(data_path)
        updated_df = pd.concat([existing_df, pd.DataFrame([applicant_details])], ignore_index=True)
        updated_df.to_csv(data_path, index=False)
        # st.session_state.form_active = False
        # st.session_state.form_submitted = False
        st.success("Applicant details successfully submitted.")
        # st.session_state.chat_history.append(AIMessage(content="The data is saved successfully."))
        # with st.chat_message("AI"):
        #     st.write("The data is saved successfully.")

# display_new_joiner_form()
print("Done Successfully")