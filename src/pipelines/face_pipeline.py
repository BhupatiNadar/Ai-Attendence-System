import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students

@st.cache_resource
def load_dlib_models():
    detector=dlib.get_frontal_face_detector()

    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec=dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector,sp,facerec

def _resize_image(img_np, max_width=500):
    """Resize image to max_width while keeping aspect ratio.
    This drastically speeds up dlib face detection on large webcam images."""
    h, w = img_np.shape[:2]
    if w <= max_width:
        return img_np
    scale = max_width / w
    new_w = max_width
    new_h = int(h * scale)
    from PIL import Image
    pil_img = Image.fromarray(img_np)
    pil_img = pil_img.resize((new_w, new_h), Image.LANCZOS)
    return np.array(pil_img)

def get_face_embedding(img_np):
    detector,sp,facerec = load_dlib_models()
    # Resize to speed up detection — the #1 cause of "stuck" UI
    img_small = _resize_image(img_np, max_width=500)
    faces = detector(img_small, 0)
    
    encodings=[]
    for face in faces:
        shape=sp(img_small,face)
        face_descriptor=facerec.compute_face_descriptor(img_small,shape,1)
        encodings.append(np.array(face_descriptor))
    return encodings

def get_trained_model():
    X=[]
    y=[]
    
    student_db=get_all_students()
    
    if not student_db:
        return None
    
    for student in student_db:
        embeddings=student.get("face_embedding")
        if embeddings:
            X.append(np.array(embeddings, dtype=np.float64))
            y.append(int(student["student_id"]))

    if len(X)==0:
        return None
    
    classifier=None
    if len(set(y)) >= 2:
        classifier=SVC(kernel="linear",probability=True,class_weight='balanced')
        try:
            classifier.fit(X,y)
        except ValueError as e:
            st.error("Error training model: " + str(e))
            classifier=None
    
    return {"clf":classifier,"X":X,"y":y}

def train_classifier():
    st.cache_resource.clear()
    model_data=get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings=get_face_embedding(class_image_np)
    
    detected_students={}
    
    model=get_trained_model()
    if not model:
        return detected_students,[],len(encodings)

    clf=model["clf"]
    X_train=model["X"]
    y_train=model["y"]
    
    all_students=sorted(list(set(y_train)))

    resemblance_threshold=0.75

    for encoding in encodings:
        best_id = None
        best_dist = float("inf")

        if clf is not None and len(all_students) >= 2:
            predicted_id=int(clf.predict([encoding])[0])
            idx = y_train.index(predicted_id)
            dist = np.linalg.norm(np.array(X_train[idx]) - np.array(encoding))
            if dist < best_dist:
                best_dist = dist
                best_id = predicted_id
        else:
            for i, emb in enumerate(X_train):
                dist = np.linalg.norm(np.array(emb) - np.array(encoding))
                if dist < best_dist:
                    best_dist = dist
                    best_id = y_train[i]
        
        if best_id is not None and best_dist <= resemblance_threshold:
            detected_students[best_id] = True

    return detected_students,all_students,len(encodings)