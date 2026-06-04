import streamlit as st

from src.database.db import create_attendence

def show_attendance_result(df,logs):
    st.write('please review attendance before confirming.')
    st.dataframe(df,hide_index=True,width='stretch')
    
    col1,col2=st.columns(2)
    
    with col1:
        if st.button('Discard',width='stretch'):
            st.session_state.attendence_images=[]
            st.session_state.voice_attendance_results=None
            st.rerun()
            
    with col2:
        if st.button("Confirm & Save",width='stretch',type='primary'):
            try:
                create_attendence(logs)
                st.toast('Attendance taken')
                st.session_state.attendence_images=[]
                st.session_state.voice_attendance_results=None
                st.rerun()
                
            except Exception as e:
                st.error('Sync failed!')
   
   
@st.dialog("Attendance Reports")
def attendence_result_dialog(df,logs):
    show_attendance_result(df,logs)