import streamlit as st 

from src.components.header import header_teacher
from src.Ui.base_layout import style_base_layout,style_background_dashboard
from src.components.teacher_screen_layout import teacher_screen_layout
from src.components.footer import footer_home

def teacher_screen():
    header_teacher()
    style_base_layout()
    style_background_dashboard()

    screen=teacher_screen_layout()

    if 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type'] = None
    
    if 'teacher_data' not in st.session_state:
        st.session_state['teacher_data'] = None

    if 'user_role' not in st.session_state:
        st.session_state['user_role'] = None

    if 'is_logged_in' not in st.session_state:
        st.session_state['is_logged_in'] = False



    match st.session_state['teacher_login_type']:
        case "register":
            screen.teacher_register_screen()
        case "login":
            screen.teacher_login_screen()
        case "dashboard":
            st.header(f'Welcome,{st.session_state['teacher_data']['username']}')
        case None:
            st.session_state['teacher_login_type'] = "login"
            st.rerun()

    footer_home()