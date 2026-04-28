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

def get_face_embedding(img_np):
    detector,sp,facerec = load_dlib_models()
    faces = detector(img_np,1)
    
    
    encodings=[]
    for face in faces:
        shape=sp(img_np,face)
        face_descriptor=facerec.compute_face_descriptor(img_np,shape,1)
        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X=[]
    y=[]
    
    student_db=get_all_students()
    
    if not student_db:
        return None
    
    for student in student_db:
        embeddings=student.get("face_embedding")
        if embeddings:
            X.append(np.array(embeddings))
            y.append(student["id"])

    if len(X)==0:
        return None
    
    classifier=SVC(kernel="linear",probability=True,class_weight='balanced')
    try:
        classifier.fit(X,y)
    except ValueError as e:
        st.error("Error training model: " + str(e))
        return None
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

    for encoding in encodings:
        if len(all_students)>=2:
            predicted=int(clf.predict([encoding])[0])
        else:
            predicted_id=int(all_students[0])
        
        student_embedding=X_train[y_train.index(predicted_id)]

        best_match_score=np.linalg.norm(np.array(student_embedding)-np.array(encoding))
        
        resemblance_threshold=0.6
        
        if best_match_score <= resemblance_threshold:
                detected_students[predicted_id]=True

    return detected_students,all_students,len(encodings)