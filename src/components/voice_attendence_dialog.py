import streamlit as st
from datetime import datetime
import pandas as pd

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import Supabase
from src.components.attendence_result_dialog import show_attendance_result

@st.dialog("Voice Attendance")
def voice_attendence_dialog(selected_subject_id):
    st.write("Record audio of student saying i am present.Then AI will recognize the students")
    
    audio_data=None
    
    audio_data=st.audio_input("Record classroom audio")
    
    if st.button('Analyze Audio',width='stretch',type='primary'):
        with st.spinner('processing Audio data'):
                enroll_res=Supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_subject_id).execute()
                enrolled_student=enroll_res.data
                    
                if not enrolled_student:
                    st.warning("No Student enrolled in this Course")
                    return
                candidated_dict={
                    s['students']['student_id']:s['students']['voice_embedding']
                    for s in enrolled_student if s['students'].get("voice_embedding")
                }
                
                if not candidated_dict:
                    st.error('No enrolled students have voice profile registered')
                    return
                
                audio_bytes=audio_data.read()
                
                detected_scores=process_bulk_audio(audio_bytes,candidated_dict)
                
                
                results,attendance_to_log=[],[]
                        
                current_timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                        
                for node in enrolled_student:
                    student=node['students']
                    score=detected_scores.get(int(student['student_id']),0.0)
                    is_Present=bool(score>0)
                            
                    results.append({
                            "Name":student['name'],
                            'ID':student['student_id'],
                            'score': f"{score:.3f}" if is_Present else "-",
                            "Status":"✅ Present" if is_Present else "❌ Absent"})
                            
                    attendance_to_log.append({
                            'student_id':student['student_id'],
                            'subject_id':selected_subject_id,
                            'timestamp':current_timestamp,
                            "ispresent":bool(is_Present)})
                    
                st.session_state.voice_attendance_results=(pd.DataFrame(results),attendance_to_log)
                
    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results,logs=st.session_state.voice_attendance_results
        show_attendance_result(df_results,logs)