from dotenv import load_dotenv
import os
import streamlit as st
from groq import Groq
import base64
import fitz
# Load environment variables
load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Pdf Tester", page_icon=":books:", layout="wide")
st.title("📚 Chat with Groq - Chapter Assistant")
st.header("Ask your question about any chapter")


classes = os.listdir("classes")
cls = st.selectbox("Select your class", classes)


subjects = os.listdir(f"classes/{cls}")
subject = st.selectbox("Select your subject", subjects)


chapters = os.listdir(f"classes/{cls}/{subject}")
chapter = st.selectbox("Select your chapter", chapters)

col1,col2 = st.columns([2,1])
pdf_path = f"classes/{cls}/{subject}/{chapter}"
with col1:
    # st.write(f"📝 You selected: **{chapter}**")
    if chapter and os.path.isfile(pdf_path):
        st.write("📄 Here is the PDF of the chapter you selected:")
        with open(pdf_path, "rb") as p:
            base64_pdf = base64.b64encode(p.read()).decode("utf-8")
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.warning("Selected chapter is not a valid PDF file.")



       
if chapter:
    # with col2:
    doc = fitz.open(pdf_path)
    fulltext =[]
    
    
with col2:    
    user_query = st.chat_input("💬 Enter your question here")
    prompt =f"""ROLE = YOU ARE A EXPERT IN Tutering you have experience of tutering and ask worderful question from student 
    TASK = You have following task:
            1.your task is to read given text and ask question related to text.  
            2.your there are 30 question realted to it.If user give correct answer than you have to appreciate it
            3.if user have any query you solve it and ask about next question
            4.if all question are completed and user give correct answer than you have to appreciate it and ask for any query  

    if user give answer or give query user query = {user_query}"""    
with col2:
    if user_query:
        client = Groq( api_key=os.environ.get("GROQ_API_KEY"),)
        with st.spinner("Thinking..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": user_query}
                ],
                model="llama-3.3-70b-versatile",
            )

            with st.chat_message('assistant'):
                     
                st.markdown(f"""
        <div style='max-height:600px;
        width:100%; overflow-y:auto; padding:10px; border:1px solid #ccc; border-radius:10px; '>
        {chat_completion.choices[0].message.content}
        </div>""",unsafe_allow_html=True)
                