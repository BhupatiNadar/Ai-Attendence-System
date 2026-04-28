import streamlit as st 

from src.components.header import header_student
from src.Ui.base_layout import style_base_layout,style_background_dashboard
from src.components.footer import footer_home
from src.components.Student_screen_layout import StudentScreenLayout

def student_screen():
    header_student()
    style_base_layout()
    style_background_dashboard()

    screen=StudentScreenLayout()
    screen.StudentLogin()
    footer_home()
