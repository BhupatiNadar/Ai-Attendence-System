import streamlit as st  
from PIL import Image
import numpy as np
class StudentScreenLayout:
    def __init__(self):
        pass
    
    def StudentLogin(self):
        st.header("Login using FaceID",text_alignment="center")
        uploaded_file = st.camera_input("Upload your image", key="student_image")
        if uploaded_file is not None:
            img=Image.open(uploaded_file)
            img_array=np.array(img)
        else:
            st.info("Please upload an image")
