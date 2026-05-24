# Interview Conductor + Interview Scorer (Group 4)

## Overview

This project implements two AI modules for a career development platform:

### Module A — Interview Conductor
Conducts an adaptive mock interview by generating the next question based on:
- Candidate profile
- Previous answers
- Interview round
- Target role
- ICP type

### Module B — Interview Scorer
Evaluates the complete interview transcript and generates:
- Overall score
- Scores per axis
- Gap vs hiring bar
- Weak moment
- Strong moment
- Next action recommendation

---

# Supported ICPs

## ICP-A (High Wage)

- Name: Riya Sharma
- Current Role: Final Year CS Student
- Target Role: Software Engineer
- Language: English

## ICP-B (Low Wage)

- Name: Arjun Yadav
- Current Role: Delivery Partner
- Target Role: Data Entry Executive
- Language: Hindi

---

# Project Structure

```text
interview-ai-group4/
│
├── main.py
├── README.md
├── prompt_defense.md
├── requirements.txt
├── .env
└── test_cases/
```

---

# Module A Input Schema

```json
{
  "icp_type": "high_wage",
  "target_role": "Software Engineer",
  "round_type": "screening",
  "company_tier": "startup",
  "language": "en",
  "previous_qa_pairs": []
}
```

# Module A Output Schema

```json
{
  "next_question": "",
  "question_type": "technical",
  "difficulty_level": 3,
  "reasoning": ""
}
```

---

# Module B Input Schema

```json
{
  "full_transcript": [],
  "icp_type": "high_wage",
  "target_role": "Software Engineer",
  "round_type": "screening",
  "hiring_bar": {
    "communication": 70,
    "technical": 70,
    "problem_solving": 70,
    "behavioral": 70,
    "delivery": 70
  }
}
```

# Module B Output Schema

```json
{
  "overall_score": 79,
  "scores_per_axis": {},
  "gap_vs_bar": {},
  "weak_moment": {},
  "strong_moment": {},
  "next_action": ""
}
```

---

# Adaptive Logic

Module A changes questions based on previous answers.

Example:

Answer mentions Python

↓

Follow-up asks about Python project challenges

↓

Next question asks about scaling and performance

This ensures interview difficulty increases when answers are stronger.

---

# Scoring Logic

Module B evaluates:

- Communication
- Technical
- Problem Solving
- Behavioral
- Delivery

Gap vs Bar:

```text
gap = user_score - hiring_bar
```

Negative values indicate candidate is below hiring expectations.

---

# How To Run

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

---

# Demo Cases

## ICP-A

Software Engineer Screening Interview

Expected Score:

```text
79/100
```

## ICP-B

Data Entry Executive Behavioral Interview

Expected Score:

```text
64/100
```

---

# Submission Checklist

- Module A Implemented
- Module B Implemented
- Adaptive Questioning
- Transcript Based Scoring
- English Support
- Hindi Support
- 3 Turn Interview Demo
- Strong vs Weak Candidate Comparison
- Gap vs Hiring Bar