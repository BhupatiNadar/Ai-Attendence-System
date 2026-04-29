import streamlit as st
from src.database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the detail of new subject:")
    sub_id=st.text_input("Subject ID",placeholder="CS101")
    sub_name=st.text_input("Subject Name",placeholder="Computer Science")
    sub_section=st.text_input("Subject Section",placeholder="A")

    if st.button("Create Subject Now!",type="primary",width='stretch',icon=':material/add:'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject created successfully!",icon=':material/check:')
                st.rerun()
            except Exception as e:
                st.error(f"Error:{str(e)}")
        else:
            st.warning("Please fill all the fields")
