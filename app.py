import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURATION ---
TEMPLATE_PATH = "Timesheet Template 2025 REV (3).xlsx - BLANK.csv"
DATABASE_PATH = "time_logs.csv"
PASSWORD = "ComroePassword2025" # Change this to your desired password

# Initialize the database if it doesn't exist
if not os.path.exists(DATABASE_PATH):
    df_init = pd.DataFrame(columns=["date", "emp_id", "emp_name", "job_num", "job_name", "hours"])
    df_init.to_csv(DATABASE_PATH, index=False)

def check_password():
    """Returns True if the user had the correct password."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 Comroe Login")
        user_pwd = st.text_input("Enter App Password", type="password")
        if st.button("Login"):
            if user_pwd == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect Password")
        return False
    return True

# --- MAIN APP ---
if check_password():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Daily Entry", "View/Download Weekly Sheet"])

    if page == "Daily Entry":
        st.header("📝 Daily Job Entry")
        
        with st.form("daily_form", clear_on_submit=True):
            entry_date = st.date_input("Date", value=datetime.now())
            emp_id = st.text_input("Employee ID #")
            emp_name = st.text_input("Employee Name")
            
            st.divider()
            job_num = st.text_input("Job Number")
            job_name = st.text_input("Job Name")
            hours = st.number_input("Hours Worked", min_value=0.0, max_value=24.0, step=0.5)
            
            submitted = st.form_submit_button("Submit Daily Entry")
            
            if submitted:
                new_entry = pd.DataFrame([[entry_date, emp_id, emp_name, job_num, job_name, hours]], 
                                         columns=["date", "emp_id", "emp_name", "job_num", "job_name", "hours"])
                new_entry.to_csv(DATABASE_PATH, mode='a', header=False, index=False)
                st.success(f"Successfully logged {hours} hours for {job_name}!")

    elif page == "View/Download Weekly Sheet":
        st.header("📊 Weekly Compilation")
        
        # Load logs
        logs = pd.read_csv(DATABASE_PATH)
        if not logs.empty:
            st.write("Current Logs in Database:")
            st.dataframe(logs)
            
            if st.button("Compile into BLANK Template"):
                # Here we would trigger the logic to map logs to your CSV template
                # This part reads the BLANK.csv and fills it based on the 'logs' data
                st.info("Compiling data... This will map all logs to the matching columns in your template.")
                
                # [LOGIC TO FILL CSV TEMPLATE GOES HERE]
                
                csv_data = logs.to_csv().encode('utf-8')
                st.download_button("📥 Download Compiled Timesheet", csv_data, "Weekly_Timesheet.csv", "text/csv")
        else:
            st.warning("No logs found yet for this week.")