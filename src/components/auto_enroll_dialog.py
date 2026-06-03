import streamlit as st
from src.database.config import Supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(Subject_code):
    student_id=st.session_state.student_data["student_id"]
    
    res=Supabase.table('subjects').select('subject_id,name').eq('subject_code',Subject_code).execute()
    
    if not res.data:
        st.error("Subject code not found")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
            
        return
    subject=res.data[0]
    
    check=Supabase.table('subject_students').select('*').eq("student_id",student_id).eq("subject_id",subject['subject_id']).execute()
    
    if check.data:
        st.info("Your already enrolled!")
        if st.button("Got it!"):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"Would u Like to join in **{subject["name"]}**?")
    
    col1,col2=st.columns(2)
    
    with col1:
        if st.button("No Thanks!"):
            st.query_params.clear()
            st.rerun()
        
    with col2:
        if st.button("Yes enroll now!",type='primary',width='stretch'):
            enroll_student_to_subject(student_id,subject["subject_id"])
            st.success("Joined Successfullly!")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
        return
    
    
