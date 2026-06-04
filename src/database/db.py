from src.database.config import Supabase
import streamlit as st

import bcrypt

def hashed_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(password,hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def check_teacher_exists(username):
    response=Supabase.table("teachers").select("username").eq("username",username).execute()
    if response.data:
        return True
    else:
        return False
    
def create_teacher(username,name,password):
    data={"username":username,"name":name,"password":hashed_password(password)}
    response=Supabase.table("teachers").insert(data).execute()
    return response.data
    
def teacher_login(username,password):
    response=Supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_password(password,teacher["password"]):
            return teacher
    return None

def get_all_students():
    response=Supabase.table("students").select("*").execute()
    return response.data

def create_student(name,face_embedding=None,voice_embedding=None):
    data={"name":name,"face_embedding":face_embedding,"voice_embedding":voice_embedding}
    response=Supabase.table("students").insert(data).execute()
    return response.data


def create_subject(sub_id,sub_name,sub_section,teacher_id):
    data={"subject_code":sub_id,"name":sub_name,"section":sub_section,"teacher_id":teacher_id}
    response=Supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subject(teacher_id):
    response=Supabase.table("subjects").select("*,subject_students(count),attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subject=response.data  
    for sub in subject:
        sub["total_students"]=sub.get("subject_students",[{}])[0].get("count",0) if sub.get("subject_students") else 0
        attendance=sub.get("attendance_logs",[])
        unique_sessions=len(set([log["timestamp"] for log in attendance]))
        sub["total_classes"]=unique_sessions

        sub.pop('subject_students',None)
        sub.pop('attendance_logs',None)
        
    return subject    

def enroll_student_to_subject(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    res=Supabase.table("subject_students").insert(data).execute()
    return res.data
    
def unenroll_student_to_subject(student_id, subject_id):
    res=Supabase.table("subject_students").delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()
    return res.data

def get_student_subject(student_id):
    res=Supabase.table("subject_students").select("*,subjects(*)").eq("student_id",student_id).execute()
    return res.data

def get_student_attendance(student_id):
    res=Supabase.table("attendance_logs").select("*").eq("student_id",student_id).execute()
    return res.data

def create_attendence(logs):
    res=Supabase.table("attendance_logs").insert(logs).execute()
    return res.data

def get_attendance_for_teacher(teacher_id):
    res = (
        Supabase.table("attendance_logs")
        .select("*, subjects!inner(*)")
        .eq("subjects.teacher_id", teacher_id)
        .execute()
    )
    return res.data