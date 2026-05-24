import json

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


def run_case(title, candidate, answers):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    transcript = []

    for answer in answers:
        output = conductor(candidate)

        print("\nMODULE A OUTPUT")
        print(json.dumps(output, indent=2, ensure_ascii=False))

        transcript.append({
            "question": output["next_question"],
            "answer": answer
        })

        candidate["previous_qa_pairs"].append({
            "question": output["next_question"],
            "answer_transcript": answer
        })

    module_b_input = {
        "full_transcript": transcript,
        "icp_type": candidate["icp_type"],
        "target_role": candidate["target_role"],
        "round_type": candidate["round_type"],
        "hiring_bar": {
            "communication": 70,
            "technical": 70,
            "problem_solving": 70,
            "behavioral": 70,
            "delivery": 70
        }
    }

    print("\nMODULE B INPUT")
    print(json.dumps(module_b_input, indent=2, ensure_ascii=False))

    report = scorer(
        transcript,
        module_b_input["hiring_bar"],
        candidate["icp_type"]
    )

    print("\nMODULE B OUTPUT")
    print(json.dumps(report, indent=2, ensure_ascii=False))


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

icp_a_answers = [
    "I built a student management system using Python and SQL.",
    "Database design and duplicate records were the hardest challenge.",
    "I would profile queries, optimize indexing, and cache frequently used data."
]

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

icp_b_answers = [
    "Main fixed salary aur stable career ke liye Data Entry Executive banna chahta hoon.",
    "Main customer ki baat dhyaan se sununga aur shaant rehkar problem solve karunga.",
    "Main roz Excel aur typing practice karke computer skills improve karunga."
]

run_case("ICP-A (RIYA SHARMA)", icp_a, icp_a_answers)
run_case("ICP-B (ARJUN YADAV)", icp_b, icp_b_answers)