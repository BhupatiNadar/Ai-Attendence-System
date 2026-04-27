import streamlit as st

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
                if Username=="" and Password=="":
                    st.error("Please fill all the fields")
                else:
                    # st.session_state['teacher_login_type']="dashboard"
                    # st.rerun()
                    st.success("Login Successful")
                    st.write(Username,Password)
                    
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
                if password==Confirm_password:
                    UserInput={"username":Username,"name":Name,"password":password}
                    st.write(UserInput)
                else:
                    st.error("Password and Confirm Password are not same")    
        with col2:
            if st.button("Login Here!",type="secondary",use_container_width=True,icon=":material/passkey:"):
                st.session_state['teacher_login_type']="login"
                st.rerun()