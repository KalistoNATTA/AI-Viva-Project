import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

# -----------------------------------
# GROQ CLIENT
# -----------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="VivaPrep AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 50px;
    font-size: 18px;
}

h1, h2, h3 {
    color: #00BFFF;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("🎓 VivaPrep AI")

    subject = st.selectbox(
        "Choose Subject",
        [
            "Operating Systems",
            "DBMS",
            "Computer Networks",
            "Data Structures",
            "C Programming"
        ]
    )

    topic = st.text_input(
        "Enter Topic",
        placeholder="Example: Semaphore"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    st.subheader("Select Mode")

    study_mode = st.checkbox(
        "Study Mode",
        value=True
    )

    practice_mode = st.checkbox(
        "Practice Mode",
        value=True
    )

    mock_viva_mode = st.checkbox(
        "Mock Viva Mode",
        value=True
    )

# -----------------------------------
# MAIN TITLE
# -----------------------------------

st.title("🎓 VivaPrep AI")
st.caption(
    "AI-powered engineering viva preparation assistant"
)

st.info(
    "Choose a subject, topic, and start preparing instantly."
)

# -----------------------------------
# TABS
# -----------------------------------

study_tab, practice_tab, viva_tab = st.tabs(
    [
        "📘 Study Mode",
        "📝 Practice Mode",
        "🎤 Mock Viva"
    ]
)

# ===================================
# STUDY MODE
# ===================================

with study_tab:

    if study_mode:

        st.subheader("Generate Viva Study Material")

        if st.button("Generate Viva Content"):

            if topic.strip() == "":
                st.warning(
                    "Please enter a topic."
                )

            else:

                with st.spinner(
                    "Professor is preparing study material..."
                ):

                    prompt = f"""
                    You are an engineering viva expert.

                    Subject: {subject}
                    Topic: {topic}
                    Difficulty: {difficulty}

                    Generate:

                    1. Top 10 Viva Questions
                    2. Answers to each question
                    3. Important Viva Questions
                    4. Professor Trap Questions
                    5. Important Concepts

                    Keep explanations simple and student-friendly.
                    Use proper formatting.
                    """

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content":
                                "You are an engineering viva expert."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    )

                    viva_content = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.subheader(
                        "📘 Viva Study Material"
                    )

                    st.markdown(
                        viva_content
                    )

# ===================================
# PRACTICE MODE
# ===================================

with practice_tab:

    if practice_mode:

        st.subheader(
            "📝 Practice & Evaluation"
        )

        practice_questions = [
            f"What is {topic}?",
            f"Why is {topic} important?",
            f"Explain the types of {topic}.",
            f"What are advantages of {topic}?",
            f"What are disadvantages of {topic}?"
        ]

        selected_question = st.selectbox(
            "Choose a Practice Question",
            practice_questions
        )

        student_answer = st.text_area(
            "Write Your Answer"
        )

        if st.button(
            "Evaluate My Answer"
        ):

            if student_answer.strip() == "":
                st.warning(
                    "Please write your answer."
                )

            else:

                with st.spinner(
                    "Professor is evaluating..."
                ):

                    evaluation_prompt = f"""
                    You are a strict engineering viva professor.

                    Subject: {subject}
                    Topic: {topic}

                    Question:
                    {selected_question}

                    Student Answer:
                    {student_answer}

                    Evaluate strictly.

                    Give:

                    1. Score out of 10
                    2. Strengths
                    3. Mistakes
                    4. Correct Viva Answer
                    5. Follow-up Viva Question

                    Be concise but useful.
                    """

                    response = (
                        client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "system",
                                    "content":
                                    "You are a strict viva professor."
                                },
                                {
                                    "role": "user",
                                    "content":
                                    evaluation_prompt
                                }
                            ]
                        )
                    )

                    evaluation = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.subheader(
                        "📊 Evaluation"
                    )

                    st.markdown(
                        evaluation
                    )

# ===================================
# MOCK VIVA MODE
# ===================================

with viva_tab:

    if mock_viva_mode:

        st.subheader(
            "🎤 Mock Viva"
        )

        if st.button(
            "Start Mock Viva"
        ):

            with st.spinner(
                "Professor is preparing question..."
            ):

                viva_prompt = f"""
                You are a strict engineering viva professor.

                Subject: {subject}
                Topic: {topic}
                Difficulty: {difficulty}

                Ask ONLY one viva question.
                """

                response = (
                    client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content":
                                "You are a strict engineering professor."
                            },
                            {
                                "role": "user",
                                "content":
                                viva_prompt
                            }
                        ]
                    )
                )

                generated_question = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                st.session_state[
                    "mock_question"
                ] = generated_question

        if "mock_question" in st.session_state:

            st.subheader(
                "Professor Question"
            )

            st.write(
                st.session_state[
                    "mock_question"
                ]
            )

            mock_answer = st.text_area(
                "Your Viva Answer"
            )

            if st.button(
                "Submit Viva Answer"
            ):

                with st.spinner(
                    "Professor is evaluating..."
                ):

                    evaluation_prompt = f"""
                    Question:
                    {st.session_state['mock_question']}

                    Student Answer:
                    {mock_answer}

                    Evaluate strictly.

                    Give:

                    1. Score out of 10
                    2. Mistakes
                    3. Correct Answer
                    4. Follow-up Question
                    """

                    response = (
                        client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "system",
                                    "content":
                                    "You are a strict engineering viva professor."
                                },
                                {
                                    "role": "user",
                                    "content":
                                    evaluation_prompt
                                }
                            ]
                        )
                    )

                    result = (
                        response
                        .choices[0]
                        .message
                        .content
                    )

                    st.subheader(
                        "📋 Professor Evaluation"
                    )

                    st.markdown(result)