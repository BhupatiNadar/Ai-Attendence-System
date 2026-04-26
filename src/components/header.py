import streamlit as st
import os
import base64

def header_home():
    
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    logo_path = os.path.join(base_path, "src", "assets", "logo.png")
    

    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    st.markdown(f"""
                <div style="text-align:center; margin-top:50px">
                    <img src="data:image/png;base64,{img_base64}" height="100px" style="display:block; margin:0 auto; border-radius:1rem"/>
                    <h1 style="text-align:center">Smart Attendance</h1>
                </div>
                """, unsafe_allow_html=True)