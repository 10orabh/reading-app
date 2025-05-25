from dotenv import load_dotenv
import os
import streamlit as st
from groq import Groq
from PIL import Image
import io
import fitz


# Load environment variables
load_dotenv()

# Streamlit UI
st.set_page_config(page_title="Pdf Tester", page_icon=":books:", layout="wide")
st.title("📚 Chat with Groq - Chapter Assistant")
st.header("Ask your question about any chapter")


sems = os.listdir("semester")
sem = st.selectbox("Select your semester",sems)


subjects = os.listdir(f"semester/{sem}")
subject = st.selectbox("Select your subject", subjects)


units = os.listdir(f"semester/{sem}/{subject}")
unit = st.selectbox("Select your unit", units)

    

pdf_path = f"semester/{sem}/{subject}/{unit}"


st.markdown(
    """
    <style>
    .st-key-pdf_container{
        
        width: 55%;
        
        
        
        padding: 20px;
        border: 1px solid #ddd; 
        border-radius: 10px;
        overflow-y: auto;
    }

    .st-key-Nxt_button{    

    
        
    </style>""",unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .st-key-inpt{
        position:fixed;
        bottom:60px;
        right:30px;
        z-index:1000;
        width: 40%;
        height: 10px;
        
    }
    .st-key-Nxt_button{
        position:relative;
        left : 150px;
        }
    .st-key-open_button{
        display:none;
        position:fixed;
        bottom:2px;
        right:20px;
        z-index:1000;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        }
    </style>
    """, unsafe_allow_html=True
)    
pdf_container = st.container(key='pdf_container')
pdf_column,ai_column = st.columns([1,3])
with pdf_column:
    with pdf_container: # st.write(f"📝 You selected: **{chapter}**")
        if unit and os.path.isfile(pdf_path):
            st.write("📄 Here is the PDF of the chapter you selected:")
            doc = fitz.open(pdf_path)
            total_pages = len(doc) 
            if "page_num" not in st.session_state:
                st.session_state.page_num = 0
            previous,curruent,next = st.columns([1,1,1])
            with previous:
                if st.button("Previous",key=f'prev_btn')and st.session_state.page_num>0:
                    st.session_state.page_num -= 1
                    st.markdown(
                    """
                    <style>
                    .st-key-ai_container {
                        display: none;
                        
                        }
                    </style>
                    """, unsafe_allow_html=True
                )
            with next:
                if st.button("Next",key='Nxt_button') and st.session_state.page_num<total_pages-1:
                    st.session_state.page_num += 1
                    st.markdown(
                    """
                    <style>
                    .st-key-ai_container {
                        display: none;
                        
                        }
                    </style>
                    """, unsafe_allow_html=True
                )
            with curruent:
                st.write(f"Page{st.session_state.page_num + 1}")

            page = doc[st.session_state.page_num]
            pix = page.get_pixmap(matrix = fitz.Matrix(2,2))
            img  = Image.open(io.BytesIO(pix.tobytes("png")))
            st.image(img,use_container_width=True)

        else:
            st.warning("Selected chapter is not a valid PDF file.")






       
if unit:
    # with col2:
    doc = fitz.open(pdf_path)
    fulltext =[]
# sticky chatbot banana
st.markdown(
    """
    <style>
    .st-key-ai_container{
        
        width: 40%;
        position:fixed;
        bottom:100px;
        right:30px; 
        z-index:1000;
        background-color: #0E1117;
        padding: 20px;
        border: 1px solid #ddd; 
        border-radius: 10px;
        overflow-y: auto;
        max-height: 80%;

    
        
    }
    </style>""",unsafe_allow_html=True
)


   
with ai_column:
    openButton = st.button("Open",key='open_button')
    if 'older_query' not in st.session_state:
        st.session_state.older_query = ""  
    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""  # Initialize the session state variable
    def clear_text():
        st.session_state.user_query = st.session_state.inpt
        st.session_state.older_query += st.session_state.inpt
        st.session_state.inpt = ""  # Clear the input field
    

    user_query = st.text_input("what's your question",key='inpt',on_change=clear_text,placeholder="Type your question here...")

    prompt2 =f"""ROLE = YOU ARE A EXPERT TUTOR WITH EXTENSIVE EXPERIENCE IN TEACHING AND ASKING THOUGHT-PROVOKING QUESTIONS TO STUDENTS.
    TASK = YOU HAVE THE FOLLOWING TASKS:
        older chat = { st.session_state.older_query}
        1.if the older chat is not empty you answer so you first check if {st.session_state.user_query} is correct respond to it
        2.else READ THE GIVEN {st.session_state.user_query} AND explain it with experiment.
        ADDITIONAL GUIDELINES:
    RESPOND IN THE SAME LANGUAGE AS THE USER'S QUERY.
    KEEP THE TONE FRIENDLY AND ENCOURAGING.
    USE EVERYDAY LANGUAGE TO MAKE THE CONVERSATION FLOW SMOOTHLY.""" 
        
        
           
        
    
    prompt =f"""ROLE = YOU ARE A EXPERT TUTOR WITH EXTENSIVE EXPERIENCE IN TEACHING AND ASKING THOUGHT-PROVOKING QUESTIONS TO STUDENTS.
    TASK = YOU HAVE THE FOLLOWING TASKS:
        1.READ THE GIVEN TEXT AND ASK QUESTIONS RELATED TO IT IN A LANGUAGE THAT IS EASY TO UNDERSTAND, JUST LIKE A DAILY CONVERSATION. FOR EXAMPLE, IF THE USER ASKS IN HINGLISH, RESPOND IN HINGLISH, LIKE A WHATSAPP CHAT, NOT IN FORMAL HINDI OR ENGLISH, BUT IN A MIX OF BOTH LANGUAGES.
        2.THERE ARE 30 QUESTIONS RELATED TO THE TEXT. IF THE USER ANSWERS CORRECTLY, APPRECIATE THEIR RESPONSE AND  MOVE ON TO THE NEXT QUESTION.
        3.IF THE USER HAS ANY QUERIES, RESOLVE THEM AND THEN ASK THE NEXT QUESTION.
        4.ONCE ALL QUESTIONS ARE COMPLETED, IF THE USER HAS ANSWERED MOST QUESTIONS CORRECTLY, APPRECIATE THEIR EFFORTS AND ASK IF THEY HAVE ANY FURTHER QUERIES.   
        USER QUERY = {user_query}
    ADDITIONAL GUIDELINES:
    RESPOND IN THE SAME LANGUAGE AS THE USER'S QUERY.
    KEEP THE TONE FRIENDLY AND ENCOURAGING.
    USE EVERYDAY LANGUAGE TO MAKE THE CONVERSATION FLOW SMOOTHLY."""    
    if st.session_state.user_query:
         # Check if the user has entered a query
        current = st.session_state.get('ai_button')
        st.session_state.ai_button = True
    
        # st.session_state.ai_button = True
        ai_container = st.container(key='ai_container')
        client = Groq( api_key=os.environ.get("GROQ_API_KEY"),)


        with ai_container:


            with st.spinner("Thinking..."):
                chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "user", "content": prompt2},
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                response = chat_completion.choices[0].message.content
                close = st.button("Close",key='close_button')
                if close:
                    
                    st.markdown(
                        """
                        <style>
                        .st-key-ai_container{
                            display:none;
                        }
                        .st-key-open_button{
                            display:block;
                        }
                        </style>
                        """, unsafe_allow_html=True
                    )
                
                        
                    
                st.chat_message('assistant').write(response)       
                    

    
            
        

