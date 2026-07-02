import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os,json,datetime

load_dotenv()

client=Groq()

st.title("AI QUIZ GENERATOR")


#---Session State Setup----
if "questions" not in st.session_state:
    st.session_state.questions=None
if "current_q" not in st.session_state:
    st.session_state.current_q=0
if "score" not in st.session_state:
    st.session_state.score=0
if "answered" not in st.session_state:
    st.session_state.answered=False


#---Functions---
def generate_quiz(topic,num_questions):
    response=client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[{
            "role":"system","content":f"""Return only a JSON array of {num_questions} MCQ Questions on {topic}.
            Each Object:question,options(4 strings),answer ,explanation.NO Markdown."""
        },{
            "role":"user","content":f"""Generate Quiz on topic:{topic} """
        }]
    )

    raw=response.choices[0].message.content
    clean=raw.replace("```json","").replace("```","").strip()
    return json.loads(clean)

def log_result(topic,score,total):
    logs=[]
    if os.path.exists("quiz_log.json"):
        with open("quiz_log.json") as f:
            logs=json.load(f)

    logs.append({"topic":topic,"score":score,"total":total,"date":str(datetime.datetime.now())})

    with open("quiz_log.json","w") as f:
        json.dump(logs,f,indent=2)        

#---Sidebar Setup---
with st.sidebar:
    st.header("New Quiz")
    topic = st.text_input("Topic: ")
    num = st.slider("questons", 3, 10, 15)
    if st.button("Generate Quiz"):
        with st.spinner("Generating..."):
            st.session_state.questions = generate_quiz(topic, num)
            st.session_state.current_q = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.session_state.topic = topic
        st.rerun()

#---Show Past Results---
st.header("Past Results")
if os.path.exists("quiz_log.json"):
    with open("quiz_log.json","r") as f:
        for entry in json.load(f)[-5:]:
            st.write(f"{entry['topic']}:{entry['score']/entry['total']}")


#---Main Quiz Display---
if st.session_state.questions:
    qs=st.session_state.questions
    i=st.session_state.current_q

    if i<len(qs):
        q=qs[i]
        st.subheader(f"Q{i+1}/{len(qs)}:{q['question']}")
        choice=st.radio("Choose:",q['options'],key=f"q{i}")

        if not st.session_state.answered:
            if st.button("Submit"):
                st.session_state.answered=True
                if choice == q['answer']:
                    st.session_state.score+=1
                st.rerun()
        else:
            if choice ==q['answer']:
                st.success("Correct!")
            else:
                st.error(f"Wrong. Correct:{q['answer']}")
            st.info(q['explanation'])
            if st.button("Next"):
                st.session_state.current_q+=1
                st.session_state.answered=False
                st.rerun()

    else:
        st.success(f"Quiz Done! Score:{st.session_state.score}/{len(qs)}")
        if st.button("Save & Finish"):
            log_result(st.session_state.topic,st.session_state.score,len(qs))
            st.session_state.questions=None
            st.rerun()
else:
    st.write("Enter a Topic in Sidebar and click Generate Quiz to start!")                



        