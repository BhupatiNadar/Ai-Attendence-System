import streamlit as st

from src.database.db import create_teacher,check_teacher_exists,teacher_login

def register_teacher(Username,Name,password,Confirm_password):
    if not Username or not Name or not password or not Confirm_password:
        return False,"All fields are required"
    if check_teacher_exists(Username):
        return False,"Teacher already exists"
    if password!=Confirm_password:
        return False,"Password and Confirm Password are not same"
    try:
        create_teacher(Username,Name,password)
        return True,"Teacher created successfully!,Login Now"
    except Exception as e:
        return False,str(e)
 
def login_teacher(Username,Password):
    if not Username or not Password:
        return False,"All fields are required"
    try:
        teacher=teacher_login(Username,Password)
        if teacher:
            return True,"Teacher logged in successfully!"
        else:
            return False,"Teacher not found"
    except Exception as e:
        return False,str(e)

class teacher_screen_layout():

    def __init__(self):
        pass

    ## ------------------------------------------------------------------------------------------------- ##

    def teacher_login_screen(self):
        Username=st.text_input("Enter Your Username:",placeholder="@bhupathi2006",max_chars=20)
        Password=st.text_input("Enter Your Password:",placeholder="password",type="password")

        st.markdown('<div style="border:1px solid lightgrey; margin-top:1rem;margin-bottom:1rem;"></div>', unsafe_allow_html=True)    

        col1,col2=st.columns(2)
        with col1:
            if st.button("Login Here!",type="primary",shortcut="Enter",use_container_width=True,icon=":material/passkey:"):
                success,message=login_teacher(Username,Password)
                if success:
                    st.success(message)
                    st.toast("Welcome Back!",icon=":material/waving_hand:")
                    import time
                    time.sleep(2)
                    st.session_state['teacher_login_type']="dashboard"
                    st.session_state['teacher_data']={'username':Username}
                    st.session_state['user_role']="teacher"
                    st.session_state['is_logged_in']=True
                    st.rerun()
                else:
                    st.error(message)    
                    
        with col2:
            if st.button("Register instead!",type="secondary",use_container_width=True,icon=":material/person_add:"):
                st.session_state['teacher_login_type']="register"
                st.rerun()

    ## ------------------------------------------------------------------------------------------------- ##


    def teacher_register_screen(self):
        Username=st.text_input("Enter Your Username:",placeholder="@bhupathi2006",max_chars=20)
        Name=st.text_input("Enter Your Name:",placeholder="V.Bhupathi")
        password=st.text_input("Enter Your password:",placeholder="password",type="password")
        Confirm_password=st.text_input("Enter Your Confirm password:",placeholder="confirm password",type="password")
        
        st.markdown('<div style="border:1px solid lightgrey; margin-top:1rem;margin-bottom:1rem;"></div>', unsafe_allow_html=True)    

        col1,col2=st.columns(2)
        with col1:
            if st.button("Register Here!",type="primary",shortcut="Enter",use_container_width=True,icon=":material/person_add:"):
                success,message=register_teacher(Username,Name,password,Confirm_password)
                if success:
                    st.success(message)
                    import time
                    time.sleep(2)
                    st.session_state['teacher_login_type']="login"
                    st.rerun()
                else:
                    st.error(message)    
        with col2:
            if st.button("Login Here!",type="secondary",use_container_width=True,icon=":material/passkey:"):
                st.session_state['teacher_login_type']="login"
                st.rerun()