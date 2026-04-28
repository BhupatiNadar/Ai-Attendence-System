from src.database.config import Supabase

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
        