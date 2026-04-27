import streamlit as st
import os
import base64

def header_home():
    
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    logo_path = os.path.join(base_path, "src", "assets", "logo.png")
    

    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
                <div style="text-align:center; margin-top:30px">
                    <img src="data:image/png;base64,{img_base64}" height="100px" style="display:block; margin:0 auto; border-radius:1rem"/>
                    <h1 style="text-align:center;font-size:30px !important;">Smart Attendance</h1>
                </div>
                """, unsafe_allow_html=True)

def header_teacher():  
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    logo_path = os.path.join(base_path, "src", "assets", "logo.png")
    
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap');
        div[data-testid="stHorizontalBlock"]:first-of-type {
            justify-content: space-between;
            align-items: center;
        }
        p{
        font-size:15px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 2])

    with col1:
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; margin-top:10px">
                <img src="data:image/png;base64,{img_base64}" height="100px" style="border-radius:1rem"/>
                <div style="font-size:28px; font-weight:700; line-height:1.2; margin:0; font-family:'Lobster Two', sans-serif;">Smart <br>Attendance</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        if st.button(label="Go Back To Home Page", key="logout", type="secondary", shortcut="Ctrl+Backspace"):
            st.session_state["login_type"] = None
            st.session_state["teacher_login_type"] = None
            st.rerun()
    if st.session_state['teacher_login_type']=="register":
        st.markdown("""
        <div style="text-align:center; margin-top:10px">
        <h4>Register Your Teacher Profile</h4></div>
        """, unsafe_allow_html=True)
    elif st.session_state['teacher_login_type']=="login":
        st.markdown("""
        <div style="text-align:center; margin-top:10px">
        <h4>Login Your Teacher Profile</h4></div>
        """, unsafe_allow_html=True) 
    elif st.session_state['teacher_login_type']=="dashboard":
        st.markdown("""
        <div style="text-align:center; margin-top:10px">
        <h4>Teacher Dashboard</h4></div>
        """, unsafe_allow_html=True) 