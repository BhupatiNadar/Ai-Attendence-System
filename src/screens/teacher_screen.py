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

    match st.session_state['teacher_login_type']:
        case "register":
            screen.teacher_register_screen()
        case "login":
            screen.teacher_login_screen()
        case None:
            st.session_state['teacher_login_type'] = "register"
            st.rerun()

    footer_home()