import streamlit as st  
from PIL import Image
import numpy as np
import hashlib
import time

from src.pipelines.face_pipeline import predict_attendance,get_face_embedding,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students,create_student,get_student_subject,get_student_attendance,unenroll_student_to_subject
from src.components.enroll_dialog import enrolled_dialog

from src.components.subject_card import subject_card

def StudentLogin():
    st.header("Login using FaceID",text_alignment="center")
    uploaded_file = st.camera_input("Upload your image", key="student_image")
    if uploaded_file is not None:
        img_bytes = uploaded_file.getvalue()
        img_hash = hashlib.md5(img_bytes).hexdigest()
        
        if "last_img_hash" not in st.session_state or st.session_state.last_img_hash != img_hash:
            img = Image.open(uploaded_file)
            img_array = np.array(img)
                
            with st.status("🔍 Scanning your face...", expanded=True) as status:
                try:
                    st.write("⏳ Loading AI models...")
                    detected, all_ids, num_faces = predict_attendance(img_array)
                    st.write(f"✅ Scan complete — {num_faces} face(s) found")
                    status.update(label="✅ Scan complete!", state="complete", expanded=False)
                except Exception as e:
                    st.write(f"❌ Error: {e}")
                    status.update(label="❌ Scan failed", state="error", expanded=True)
                    detected, all_ids, num_faces = {}, [], 0
                    
            st.session_state.last_img_hash = img_hash
            st.session_state.last_scan_result = (detected, all_ids, num_faces)
            st.session_state.last_img_array = img_array
        else:
            detected, all_ids, num_faces = st.session_state.last_scan_result
            img_array = st.session_state.last_img_array

        show_registration = False
        if num_faces == 0:
            st.error("No face detected. Please try again.")
        elif num_faces > 1:
            st.error("Multiple faces detected. Please ensure only one person is in the frame.")
        else:
            if detected:
                student_id = list(detected.keys())[0]
                all_students = get_all_students()
                student = next((s for s in all_students if str(s["student_id"]) == str(student_id)), None)

                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = "student"
                    st.session_state.student_data = student
                    st.toast(f"Welcome back, {student['name']}!", icon="👋")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Face not recognized. New here? Please register below.")
                    show_registration = True
            else:
                st.warning("Face not recognized. New here? Please register below.")
                show_registration = True

            if show_registration:
                with st.container():
                    st.header("Register for face ID",text_alignment="center")
                    new_name=st.text_input("Enter your name", placeholder="Eg : Bhupathi Nadar")

                    st.subheader("Optional:Voice Enrollment")
                    st.info("Enroll your voice for attendance")
                    audio_data=None

                    try:
                        audio_data=st.audio_input("Record a short phrase like i am present,My name is Bhupati")
                    except Exception as e:
                        st.error(f"Error recording audio: {e}")
                    
                    if st.button("Create Account",type="primary"):
                        if new_name:
                            with st.spinner("creating profile"):
                                try:
                                    embedding=get_face_embedding(img_array)

                                    if embedding and len(embedding)>0:
                                        embedding_data=embedding[0].tolist()
                                        voice_embedding=None
                                        if audio_data:
                                            voice_embedding=get_voice_embedding(audio_data.read())
                                        
                                        response_data=create_student(
                                            name=new_name,
                                            face_embedding=embedding_data,
                                            voice_embedding=voice_embedding
                                        )

                                        if response_data:
                                            train_classifier()
                                            for key in ["last_img_hash", "last_scan_result", "last_img_array"]:
                                                st.session_state.pop(key, None)
                                            st.toast("Profile created successfully",icon="✅")
                                            st.session_state.is_logged_in=True
                                            st.session_state.user_role="student"
                                            st.session_state.student_data=response_data[0]
                                            st.toast(f"Profile created! ,Hi {new_name}!")
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.error("couldn't capture your facial feature for registrations",icon="❌")
                                    
                                except Exception as e:
                                    st.error(f"Error creating face ID: {e}")
                                    
                        else:
                            st.error("Name field is empty")
    else:
        st.info("Please upload an image")

def student_dashboard():
    st.header("Student Dashboard",text_alignment="center")
    student_data=st.session_state.student_data
    student_data.pop("face_embedding",None)
    student_data.pop("voice_embedding",None)
    # st.write(student_data)
    st.markdown(
    f"""
    <style>
    .welcome-text {{
        font-size: 32px;
        color: #000000;
        font-weight: bold;
        margin:10px;
    }}
    </style>

    <div class="welcome-text">
        Welcome back {st.session_state.student_data['name']}
    </div>
    """,
    unsafe_allow_html=True
)

    col1,col2=st.columns(2)
    with col1:
        st.header('your Enrolled Subjects')
    with col2:
        if st.button('Enroll in Subjects',type='primary',width='stretch'):
            enrolled_dialog()

    st.divider()
    
    with st.spinner('Loading your enrolled subjects...'):
        subjects=get_student_subject(student_data['student_id'])
        logs=get_student_attendance(student_data['student_id'])
        
    stats_map={}
    
    for log in logs:
        sid=log['subject_id']
        
        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
            
        stats_map[sid]["total"]+=1
        
        if logs.get('is_present'):
            stats_map[sid]['attended']+=1
            
        
    cols=st.columns(2)
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub['subject_id']
        
        
        stats=stats_map.get(sid,{"total":0,"attended":0})
        
        def unenroll_button():
            if st.button('Unenroll from this course', type="tertiary",width="stretch",icon=":material/delete_forever:",key=f"unenroll_{sid}"):
                unenroll_student_to_subject(st.session_state.student_data["student_id"],sid)
                st.rerun()
        
        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                subject_code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("🗓️","Total",stats['total']),
                    ("✅","Attendence",stats['attended'])
                ],
                footer_callback=unenroll_button
            )
            
        
        
