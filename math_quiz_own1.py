import streamlit as st
import random
import json

st.title("📝 Grade 5 Maths Quiz")
#st.write("Select the correct answer and click submit button at the bottom!")

with open(".\\maths quiz questions.json", "r") as file:
    all_questions = json.load(file)

# ---------- Initialize Session State ----------
if "started" not in st.session_state:
    st.session_state.started = False
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "selected_questions" not in st.session_state:
    st.session_state.selected_questions = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# ---------- Step 1: Select number of questions ----------
if not st.session_state.started:
    max_q = len(all_questions)
    num = st.slider("🔢 Select number of questions you want to attempt:", 1, max_q, 5)
    if st.button("🚀 Start Quiz"):
        st.session_state.selected_questions = random.sample(all_questions, num)
        st.session_state.started = True
        st.rerun()  # refresh to start quiz cleanly

# ---------- Step 2: Display questions one-by-one ----------
elif st.session_state.q_index < len(st.session_state.selected_questions):
    q = st.session_state.selected_questions[st.session_state.q_index]
    st.subheader(f"Question {st.session_state.q_index + 1} of {len(st.session_state.selected_questions)}")
    st.write(q["question"])
    user_answer = st.radio("Choose your answer:", q["options"], key=st.session_state.q_index)

    if st.button("Next"):
        st.session_state.answers.append(user_answer)
        if user_answer == q["answer"]:
            st.session_state.score += 1
        st.session_state.q_index += 1
        st.rerun()

# ---------- Step 3: Show score and explanations ----------
else:
    st.markdown("### 🎯 Quiz Complete!")
    st.success(f"Your score: **{st.session_state.score} / {len(st.session_state.selected_questions)}**")

    st.markdown("### 📘 Review Incorrect Answers")
    for i, q in enumerate(st.session_state.selected_questions):
        selected = st.session_state.answers[i]
        if selected != q["answer"]:
            st.write(f"**Q{i+1}: {q['question']}**")
            st.write(f"Your answer: {selected}")
            st.write(f"Correct answer: {q['answer']}")
            explanation = q.get("explanations", {}).get(selected, "No explanation available.")
            st.info(f"💡 Explanation: {explanation}")

    # Optional restart
    if st.button("🔄 Restart Quiz"):
        for key in ["started", "q_index", "selected_questions", "score", "answers"]:
            st.session_state.pop(key)
        st.rerun()