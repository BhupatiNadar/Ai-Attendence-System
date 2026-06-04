import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.components.auto_enroll_dialog import auto_enroll_dialog

def main():
    st.set_page_config(
        page_title='Ai Attendence system make Attendance faster'
    )
    # Teacher/Student login type
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # User role
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None

    # Teacher register/login/dashboard type
    if 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type'] = None
    
    # Teacher data
    if 'teacher_data' not in st.session_state:
        st.session_state['teacher_data'] = None

    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

    # Student data
    if 'student_data' not in st.session_state:
        st.session_state['student_data'] = None

    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()
            
        case "student":
            student_screen()
            
        case None:
            home_screen()
            
    
    join_code=st.query_params.get("join-code")
    if join_code:
        if st.session_state.login_type != "student":
            st.session_state.login_type="student"
            st.rerun()
        if st.session_state.get("is_logged_in") and st.session_state.get('user_role') == "student":
            auto_enroll_dialog(join_code)
main()