import streamlit as st
from src.database.config import Supabase
from src.database.db import enroll_student_to_subject
import time

@st.dialog("Enroll for Subjects")
def enrolled_dialog():
    st.write("Enter the subjects code provided by the teacher to enroll")
    join_code=str(st.text_input('subject code',placeholder='Eg. CS101'))
    if st.button("Enroll Now",type="primary",width='stretch'):
        if join_code:
            res=Supabase.table("subjects").select("*").eq("subject_code",join_code).execute()
            if res.data:
                subject=res.data[0]
                student_id=st.session_state.student_data['student_id']
                check=Supabase.table('subject_students').select('*').eq("student_id",student_id).eq("subject_id",subject['subject_id']).execute()
                if check.data:
                    st.warning("You are already enrolled in this subject")
                else:
                    enroll_student_to_subject(student_id,subject['subject_id'])
                    st.success("succesfully enrolled in the subject")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Subject not found")
        else:
            st.warning("Please enter the subject code")
