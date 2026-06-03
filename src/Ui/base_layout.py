import streamlit as st

def style_base_layout():
    
    st.markdown("""
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap');
                    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400..700;1,400..700&family=Lobster+Two:ital,wght@0,400;0,700;1,400;1,700&display=swap');
                    # #MainMenu,header,footer{
                    #     visibility:hidden;
                    # }
                    
                    .block-container{
                        padding-top:1.5rem;
                    }
                    
                    h1,h2{
                        font-family:'Lobster Two',sans-serif !important; 
                        font-size:4rem !important;
                        line-height:1.1 !important;
                        margin-bottom:0rem !important;
                        color:#30364F !important;
                    }
                    
                    h3,h4,p {
                        font-family:'Libre Baskerville',sans-serif !important; 
                    }
                    
                    button{
                        background-color:#9AD872 !important;
                        color:white !important;
                        border-radius:1.5rem !important;
                        padding:10px 20px !important;
                        border:None !important;
                        transition: transform 0.25s ease-in-out !important;
                    }
                    
                    button[kind="secondary"]{
                        background-color:#FF8383 !important;
                        color:white !important;
                        border-radius:1.5rem !important;
                        padding:10px 20px !important;
                        border:None !important;
                        transition: transform 0.25s ease-in-out !important;
                    }
                    
                    button[kind="tertiary"]{
                        background-color:#080616 !important;
                        color:white !important;
                        border-radius:1.5rem !important;
                        padding:10px 20px !important;
                        border:None !important;
                        transition: transform 0.25s ease-in-out !important;
                    }
                    
                    button:hover{
                        transform:scale(1.05)
                    }
                
                </style>
                """,unsafe_allow_html=True)
    
    
def style_background_home():
    
    st.markdown("""
                <style>
                
                    .stApp{
                        background:#FAFFCB !important;
                        
                    }
                    
                    div[data-testid="stColumn"]:nth-of-type(1),div[data-testid="stColumn"]:nth-of-type(3){
                        background-color:#CFECF3 !important;
                        border-radius:1.5rem !important;
                        padding:2rem !important;
                        color:#000000 !important;
                    }
                </style>
                """,unsafe_allow_html=True)
    
    
def style_background_dashboard():
    
    st.markdown("""
                <style>
                
                    .stApp{
                        background:#CFECF3 !important;
                    }

                    h2{
                        font-size:2rem !important;
                    }
                </style>
                """,unsafe_allow_html=True)
    