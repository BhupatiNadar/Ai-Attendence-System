import streamlit as st 

from src.components.header import header_teacher
from src.Ui.base_layout import style_base_layout,style_background_dashboard
from src.components.teacher_screen_layout import teacher_register_screen,teacher_login_screen,teacher_dashboard_screen
from src.components.footer import footer_home

def teacher_screen():

    match st.session_state['teacher_login_type']:
        case "register":
            header_teacher()
            style_base_layout()
            style_background_dashboard()
            teacher_register_screen()
        case "login":
            header_teacher()
            style_base_layout()
            style_background_dashboard()
            teacher_login_screen()
        case "dashboard":
            header_teacher()
            style_base_layout()
            style_background_dashboard()
            teacher_dashboard_screen()
        case None:
            st.session_state['teacher_login_type'] = "login"
            st.rerun()

    footer_home()