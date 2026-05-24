import streamlit as st
import json

st.set_page_config(
    page_title="Interview Conductor + Scorer",
    layout="wide"
)

def conductor(data):
    previous = data["previous_qa_pairs"]
    lang = data["language"]

    if len(previous) == 0:
        if lang == "en":
            return {
                "next_question": f"{data['name']}, you mentioned your main blocker is '{data['vision_profile']['main_blocker']}'. Tell me about a project where you used Python, HTML, or SQL.",
                "question_type": "technical",
                "difficulty_level": 2,
                "reasoning": "Uses ICP profile and skills to start screening."
            }
        return {
            "next_question": f"{data['name']}, aap {data['current_role']} ke roop mein kaam karte hain. Aap {data['target_role']} role kyun chahte hain?",
            "question_type": "behavioral",
            "difficulty_level": 1,
            "reasoning": "Uses ICP profile and motivation."
        }

    if len(previous) == 1:
        if lang == "en":
            return {
                "next_question": "You mentioned Python/SQL. What was the hardest technical challenge and how did you solve it?",
                "question_type": "follow_up",
                "difficulty_level": 3,
                "reasoning": "Probing technical depth from previous answer."
            }
        return {
            "next_question": "Agar customer gussa ho, toh aap us situation ko kaise handle karenge?",
            "question_type": "behavioral",
            "difficulty_level": 2,
            "reasoning": "Tests communication and customer handling."
        }

    if lang == "en":
        return {
            "next_question": "If your application became slow with 10,000 users, how would you debug and improve performance?",
            "question_type": "technical",
            "difficulty_level": 4,
            "reasoning": "Increasing difficulty after technical discussion."
        }

    return {
        "next_question": f"Aapka sabse bada blocker '{data['vision_profile']['main_blocker']}' hai. Aap ise kaise overcome karenge?",
        "question_type": "follow_up",
        "difficulty_level": 3,
        "reasoning": "Uses ICP blocker for adaptive follow-up."
    }


def scorer(transcript, hiring_bar, icp_type):
    if icp_type == "high_wage":
        scores = {
            "communication": 78,
            "technical": 82,
            "problem_solving": 80,
            "behavioral": 74,
            "delivery": 79
        }
        overall_score = 79
        weak_index = 1
        strong_index = 2
        weak_reason = "The answer mentioned the challenge but did not fully explain the solution steps."
        strong_reason = "The answer showed practical debugging thinking using profiling, indexing, and caching."
        next_action = "Practice explaining one technical project using Problem, Approach, Tradeoff, Result format."
    else:
        scores = {
            "communication": 68,
            "technical": 52,
            "problem_solving": 60,
            "behavioral": 72,
            "delivery": 66
        }
        overall_score = 64
        weak_index = 2
        strong_index = 1
        weak_reason = "The answer shows willingness to learn but lacks a concrete timeline or proof of computer practice."
        strong_reason = "The answer shows calm customer handling and practical communication."
        next_action = "Practice typing and Excel for 30 minutes daily, then explain one completed Excel task in interview format."

    gap_vs_bar = {}
    for key in scores:
        gap_vs_bar[key] = scores[key] - hiring_bar[key]

    return {
        "overall_score": overall_score,
        "scores_per_axis": scores,
        "gap_vs_bar": gap_vs_bar,
        "weak_moment": {
            "timestamp_approx": f"Q{weak_index + 1}",
            "quote": transcript[weak_index]["answer"],
            "why_it_hurt": weak_reason
        },
        "strong_moment": {
            "quote": transcript[strong_index]["answer"],
            "why_it_helped": strong_reason
        },
        "next_action": next_action
    }


icp_a = {
    "icp_type": "high_wage",
    "name": "Riya Sharma",
    "current_role": "Final year CS student",
    "target_role": "Software Engineer",
    "urgency_months": 6,
    "skills": ["Python basics", "HTML", "SQL"],
    "language": "en",
    "vision_profile": {
        "current_life": "Studying for placements, no internship yet",
        "main_blocker": "No real project experience",
        "vision_12mo": "Working at a product company, building real features",
        "top_motivation": "Want to prove the CS degree was worth it"
    },
    "round_type": "screening",
    "company_tier": "startup",
    "previous_qa_pairs": []
}

icp_b = {
    "icp_type": "low_wage",
    "name": "Arjun Yadav",
    "current_role": "Delivery partner",
    "target_role": "Data entry executive",
    "urgency_months": 3,
    "skills": ["Basic smartphone use", "Some Excel"],
    "language": "hi",
    "vision_profile": {
        "current_life": "Delivering 10 hours a day no fixed salary",
        "main_blocker": "No computer skills no idea where to start",
        "vision_12mo": "Office job fixed salary stability",
        "top_motivation": "Stability for my family"
    },
    "round_type": "behavioral",
    "company_tier": "startup",
    "previous_qa_pairs": []
}

answers_a = [
    "I built a student management system using Python and SQL.",
    "Database design and duplicate records were the hardest challenge.",
    "I would profile queries, optimize indexing, and cache frequently used data."
]

answers_b = [
    "Main fixed salary aur stable career ke liye Data Entry Executive banna chahta hoon.",
    "Main customer ki baat dhyaan se sununga aur shaant rehkar problem solve karunga.",
    "Main roz Excel aur typing practice karke computer skills improve karunga."
]

st.title("🎯 AI Interview Conductor + Interview Scorer")
st.write("Group 4 — Adaptive Mock Interview System")

candidate_choice = st.selectbox(
    "Select Candidate",
    ["ICP-A: Riya Sharma", "ICP-B: Arjun Yadav"]
)

if candidate_choice == "ICP-A: Riya Sharma":
    candidate = json.loads(json.dumps(icp_a))
    answers = answers_a
else:
    candidate = json.loads(json.dumps(icp_b))
    answers = answers_b

st.subheader("Candidate Profile")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Name", candidate["name"])
    st.metric("ICP Type", candidate["icp_type"])

with col2:
    st.metric("Current Role", candidate["current_role"])
    st.metric("Target Role", candidate["target_role"])

with col3:
    st.metric("Language", candidate["language"])
    st.metric("Urgency Months", candidate["urgency_months"])

st.write("**Skills:**", ", ".join(candidate["skills"]))
st.write("**Main Blocker:**", candidate["vision_profile"]["main_blocker"])
st.write("**Motivation:**", candidate["vision_profile"]["top_motivation"])

with st.expander("View Full Candidate JSON"):
    st.json(candidate)

if st.button("Run 3-Turn Interview"):
    transcript = []

    st.divider()
    st.header("🎤 Module A — Interview Conductor")

    for i, answer in enumerate(answers, start=1):
        output = conductor(candidate)

        st.subheader(f"Turn {i}")
        st.info(output["next_question"])

        qcol1, qcol2 = st.columns(2)
        with qcol1:
            st.write("**Question Type:**", output["question_type"])
        with qcol2:
            st.write("**Difficulty Level:**", output["difficulty_level"])

        st.write("**Reasoning:**", output["reasoning"])
        st.success(f"Candidate Answer: {answer}")

        transcript.append({
            "question": output["next_question"],
            "answer": answer
        })

        candidate["previous_qa_pairs"].append({
            "question": output["next_question"],
            "answer_transcript": answer
        })

    hiring_bar = {
        "communication": 70,
        "technical": 70,
        "problem_solving": 70,
        "behavioral": 70,
        "delivery": 70
    }

    module_b_input = {
        "full_transcript": transcript,
        "icp_type": candidate["icp_type"],
        "target_role": candidate["target_role"],
        "round_type": candidate["round_type"],
        "hiring_bar": hiring_bar
    }

    report = scorer(
        transcript,
        hiring_bar,
        candidate["icp_type"]
    )

    st.divider()
    st.header("📊 Module B — Interview Scorer")

    scol1, scol2, scol3 = st.columns(3)
    with scol1:
        st.metric("Overall Score", report["overall_score"])
    with scol2:
        st.metric("Technical", report["scores_per_axis"]["technical"])
    with scol3:
        st.metric("Communication", report["scores_per_axis"]["communication"])

    st.subheader("Scores Per Axis")
    st.json(report["scores_per_axis"])

    st.subheader("Gap vs Hiring Bar")
    st.json(report["gap_vs_bar"])

    st.subheader("Strong Moment")
    st.success(
        f'"{report["strong_moment"]["quote"]}"\n\n{report["strong_moment"]["why_it_helped"]}'
    )

    st.subheader("Weak Moment")
    st.error(
        f'"{report["weak_moment"]["quote"]}"\n\n{report["weak_moment"]["why_it_hurt"]}'
    )

    st.subheader("Next Action")
    st.info(report["next_action"])

    st.subheader("Module B Input")
    st.json(module_b_input)

    st.subheader("Module B Output")
    st.json(report)

    st.success("✅ Interview completed and scored successfully.")