import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen

def main():
    # Teacher/Student login type
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None

    # Teacher register/login/dashboard type
    if 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type'] = None
    
    # Teacher/Student data
    if 'teacher_data' not in st.session_state:
        st.session_state['teacher_data'] = None

    # User role
    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None

    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False

        
    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()
            
        case "student":
            student_screen()
            
        case None:
            home_screen()
main()