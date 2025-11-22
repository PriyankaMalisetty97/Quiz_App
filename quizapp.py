import streamlit as st
import json
import os
from openai import OpenAI

# Load API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
@st.cache_data
@st.cache_data
def fetch_questions(text_content, quiz_level):

    RESPONSE_JSON = {
        "mcqs": [
            {
                "mcq": "multiple choice question",
                "options": {
                    "a": "choice here",
                    "b": "choice here",
                    "c": "choice here",
                    "d": "choice here",
                },
                "correct": "a"
            }
        ]
    }

    PROMPT = f"""
    You are an expert quiz generator.

    Text:
    {text_content}

    Task:
    Generate exactly 3 MCQ questions, difficulty: {quiz_level}.
    Format output as JSON exactly like the given template.
    Template:
    {json.dumps(RESPONSE_JSON, indent=2)}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": PROMPT}],
            temperature=0.3,
            max_tokens=800,
        )
    except Exception as e:
        st.error("OpenAI API Error:")
        st.code(str(e))
        return []   # ← THIS MUST BE HERE (inside the function)

    raw_output = response.choices[0].message.content

    try:
        return json.loads(raw_output)["mcqs"]
    except:
        st.error("AI returned invalid JSON:")
        st.code(raw_output)
        return []



def main():

    st.title("🧠 AI Quiz Generator (Python + Streamlit + OpenAI)")

    text_content = st.text_area("Paste the content here:")
    quiz_level = st.selectbox("Select difficulty:", ["Easy", "Medium", "Hard"]).lower()

    session_state = st.session_state

    if "quiz_generated" not in session_state:
        session_state.quiz_generated = False

    if st.button("Generate Quiz"):
        session_state.quiz_generated = True

    # When quiz is generated
    if session_state.quiz_generated:

        questions = fetch_questions(text_content, quiz_level)

        selected_options = []
        correct_answers = []

        for q in questions:
            opts = list(q["options"].values())
            selected = st.radio(q["mcq"], opts, index=None)
            selected_options.append(selected)

            # correct option value → ex: options["b"]
            correct_answers.append(q["options"][q["correct"]])

        # Submit quiz
        if st.button("Submit"):
            marks = 0
            st.header("📊 Your Results")

            for i, q in enumerate(questions):
                st.subheader(q["mcq"])
                st.write(f"Your Answer: {selected_options[i]}")
                st.write(f"Correct Answer: {correct_answers[i]}")

                if selected_options[i] == correct_answers[i]:
                    marks += 1

            st.success(f"🎯 Score: {marks} / {len(questions)}")


if __name__ == "__main__":
    main()

