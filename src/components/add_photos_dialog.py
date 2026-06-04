import streamlit as st
from PIL import Image

@st.dialog("Capture or Upload photo")
def add_photos_dialog():
    
    st.write("Add classroom photos to scan for attendance")
    
    if "photo_tab"  not in st.session_state:
        st.session_state["photo_tab"]='camera'
    
    if "_processed_photo_keys" not in st.session_state:
        st.session_state["_processed_photo_keys"]=set()
        
    t1,t2=st.columns(2)
    
    with t1:
        type_camera="primary" if st.session_state.photo_tab == "camera" else "tertiary"
        if st.button("Camera",type=type_camera,width="stretch"):
            st.session_state.photo_tab='camera'
            
    with t2:
        type_upload="primary" if st.session_state.photo_tab == "upload" else "tertiary"
        if st.button("Upload photos",type=type_upload,width="stretch"):
            st.session_state.photo_tab='upload'
        
    
    if st.session_state.photo_tab == "camera":
        cam_photo=st.camera_input("Take Snapshot",key="dialog_cam")
        if cam_photo:
            photo_key=cam_photo.file_id
            if photo_key not in st.session_state._processed_photo_keys:
                st.session_state._processed_photo_keys.add(photo_key)
                st.session_state.attendence_images.append(Image.open(cam_photo))
            st.success("Photo Captured!")
            
    if st.session_state.photo_tab == "upload":
        uploaded_files=st.file_uploader("choose image files",type=["jpg","png","jpeg"],accept_multiple_files=True,key="dialog_upload")
        
        if uploaded_files:
            for f in uploaded_files:
                file_key=f.file_id
                if file_key not in st.session_state._processed_photo_keys:
                    st.session_state._processed_photo_keys.add(file_key)
                    st.session_state.attendence_images.append(Image.open(f))
                
            st.success("Photo(s) Uploaded Successfully")
            
    st.divider()
    if st.button("Done",type="primary",width="stretch"):
        st.rerun()