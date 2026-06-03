import streamlit as st
import time

from src.database.db import create_teacher,check_teacher_exists,teacher_login,get_teacher_subject
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.add_photos_dialog import add_photos_dialog

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
            return True,"Teacher logged in successfully!",teacher
        else:
            return False,"Teacher not found"
    except Exception as e:
        return False,str(e),None


## ------------------------------------------------------------------------------------------------- ##

def teacher_login_screen():
    Username=st.text_input("Enter Your Username:",placeholder="@bhupathi2006",max_chars=20)
    Password=st.text_input("Enter Your Password:",placeholder="password",type="password")

    st.markdown('<div style="border:1px solid lightgrey; margin-top:1rem;margin-bottom:1rem;"></div>', unsafe_allow_html=True)    

    col1,col2=st.columns(2)
    with col1:
        if st.button("Login Here!",type="primary",shortcut="Enter",use_container_width=True,icon=":material/passkey:"):
            success,message,teacher_data=login_teacher(Username,Password)
            if success:
                st.success(message)
                st.toast("Welcome Back!",icon=":material/waving_hand:")
                time.sleep(2)
                st.session_state['teacher_login_type']="dashboard"
                st.session_state['teacher_data']=teacher_data
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


def teacher_register_screen():
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
                time.sleep(2)
                st.session_state['teacher_login_type']="login"
                st.rerun()
            else:
                st.error(message)    
    with col2:
        if st.button("Login Here!",type="secondary",use_container_width=True,icon=":material/passkey:"):
            st.session_state['teacher_login_type']="login"
            st.rerun()


## ------------------------------------------------------------------------------------------------- ##

def teacher_dashboard_screen():
    teacher_data=st.session_state['teacher_data']
    st.subheader(f"Welcome {teacher_data['username']}")
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state["current_teacher_tab"]="take_attendance"

    tab1,tab2,tab3=st.columns(3)

    with tab1:
        type1="primary" if st.session_state['current_teacher_tab']=="take_attendance" else "tertiary"
        if st.button("Take Attendance",width="stretch",type=type1,icon=':material/ar_on_you:',use_container_width=True):
            st.session_state["current_teacher_tab"]="take_attendance"
            st.rerun()

    with tab2:
        type2="primary" if st.session_state['current_teacher_tab']=="Manage_subjects" else "tertiary"
        if st.button("Manage Subjects",width="stretch",type=type2,icon=':material/book_ribbon:',use_container_width=True):
            st.session_state["current_teacher_tab"]="Manage_subjects"
            st.rerun()

    with tab3:
        type3="primary" if st.session_state['current_teacher_tab']=="attendance_records" else "tertiary"
        if st.button("Attendance Records",width="stretch",type=type3,icon=':material/cards_stack:',use_container_width=True):
            st.session_state["current_teacher_tab"]="attendance_records"
            st.rerun()

    st.divider()

    if st.session_state['current_teacher_tab']=="take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state['current_teacher_tab']=="Manage_subjects":
        teacher_tab_manage_subjects()
    elif st.session_state['current_teacher_tab']=="attendance_records":
        teacher_tab_attendance_records()

def teacher_tab_take_attendance():
    teacher_id=st.session_state.teacher_data["teacher_id"]
    st.markdown("### Take Attendance")
    
    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images=[]
        
    subjects=get_teacher_subject(teacher_id)
    
    if not subjects:
        st.warning('you havent created any subjects yet! please create one to begin')
        return
    
    subject_options={f"{s['name']}-{s["subject_code"]}": s['subject_id'] for s in subjects}
    
    col1,col2=st.columns([3,1])
    
    with col1:
        selected_subject_label=st.selectbox('Select Subject',options=list(subject_options.keys()))
        
    with col2:
        if st.button("Add Photos",type="primary",icon=":material/add_a_photo:",width="stretch"):
            add_photos_dialog()
    
    selected_subject_id=subject_options[selected_subject_label]
    

def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data["teacher_id"]
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage Subjects",width="stretch")
    with col2:
        if st.button("Add Subject",type="secondary",icon=":material/add:",use_container_width=True,width="stretch"):
            create_subject_dialog(teacher_id)
    
    Subjects=get_teacher_subject(teacher_id)
    if Subjects:
        for sub in Subjects:
            stats=[
                ("🫂","Students",sub["total_students"]),
                ("🕰️","Classes",sub["total_classes"]),
            ]
        def share_btn():
            if st.button(f"Share Code:{sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                share_subject_dialog(sub["name"],sub['subject_code'])
            st.space()

        subject_card(
            name=sub["name"],
            subject_code=sub["subject_code"],
            section=sub["section"],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("No Subjects found. Create one Above")
        

def teacher_tab_attendance_records():
    st.markdown("### Attendance Records")