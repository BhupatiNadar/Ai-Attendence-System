import streamlit as st 
import os
from PIL import Image

from src.components.header import header_home
from src.Ui.base_layout import style_base_layout,style_background_home
from src.components.footer import footer_home

base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
student_logo_path = os.path.join(base_path, "src", "assets", "student.png")
teacher_logo_path=os.path.join(base_path,"src","assets","teacher.png")
teacher_img = Image.open(teacher_logo_path).resize((270, 250))

def home_screen():
    header_home()
    style_base_layout()
    style_background_home()
    
    col1, empty1, col2 = st.columns([2, 0.5, 2],gap="medium")


    
    with col1:
        st.subheader("I'm Teacher")
        st.image(teacher_img, width=270)
        if st.button("Teacher Portal", type="primary", icon=":material/arrow_outward:",icon_position='right'):
            st.session_state["login_type"]="teacher"
            st.rerun()
    with col2:
        st.subheader("I'm Student")
        st.image(student_logo_path,width=250)
        if st.button("Student Portal", type="primary", icon=":material/arrow_outward:",icon_position='right'):
            st.session_state["login_type"]="student"
            st.rerun()
    footer_home()