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