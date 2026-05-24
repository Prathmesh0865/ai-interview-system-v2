# Prompt Defense – Group 4
## Interview Conductor + Interview Scorer

---

# Problem Statement

Build two connected AI modules:

1. Interview Conductor
2. Interview Scorer

The system must support:

- ICP-A (High Wage)
- ICP-B (Low Wage)

The system must adapt questions based on previous answers and provide transcript-based scoring.

---

# Prompt Design Decisions

## Module A – Interview Conductor

Goal:

Generate the next interview question based on:

- Previous answers
- ICP type
- Target role
- Language
- Interview round

Output:

```json
{
  "next_question": "",
  "question_type": "",
  "difficulty_level": 1,
  "reasoning": ""
}
```

---

### Decision 1

Use ICP information directly.

Example:

Riya Sharma:

- Software Engineer
- English
- Technical interview

Arjun Yadav:

- Data Entry Executive
- Hindi
- Behavioral interview

Reason:

Questions should feel personal and role-specific.

---

### Decision 2

Increase difficulty gradually.

Example:

Turn 1:

Project discussion

↓

Turn 2:

Challenge discussion

↓

Turn 3:

Scaling or advanced scenario

Reason:

Follows deliberate practice principles.

---

### Decision 3

Hindi questions should not be translated English.

Example:

Bad:

"Describe a conflict situation."

Good:

"Agar customer gussa ho toh aap kya karenge?"

Reason:

Low wage users need natural workplace language.

---

# Module B – Interview Scorer

Goal:

Convert transcript into structured feedback.

Output:

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

### Decision 1

Use transcript quotes.

Example:

Weak Moment:

"Database design and duplicate records were the hardest challenge."

Reason:

Assignment explicitly states weak_moment and strong_moment must quote the transcript.

---

### Decision 2

Gap vs Bar

Formula:

```text
candidate_score - hiring_bar
```

Example:

52 - 70 = -18
```

Negative values are preserved.

Reason:

Assignment explicitly states negative values must not be softened.

---

### Decision 3

Different ICP scores

High Wage Candidate:

79/100

Low Wage Candidate:

64/100

Reason:

Assignment requires different feedback for strong and weak candidate sets.

---

# What Broke Initially

## Issue 1

Same score for all candidates.

Problem:

Feedback was not differentiated.

Fix:

Created separate scoring paths for:

- high_wage
- low_wage

---

## Issue 2

Repeated Hindi questions.

Problem:

Question 2 and Question 3 were identical.

Fix:

Question 3 now uses the candidate blocker.

Example:

"No computer skills no idea where to start"

↓

"Aap ise kaise overcome karenge?"

---

## Issue 3

Generic opening questions.

Problem:

Did not use ICP profile.

Fix:

Questions now use:

- Name
- Role
- Skills
- Motivation
- Main blocker

---

# Edge Cases Tested

1. High wage technical candidate
2. High wage weak technical answer
3. High wage strong technical answer
4. Low wage Hindi candidate
5. Low wage communication focused answer
6. Missing project experience
7. Strong problem solving answer
8. Weak communication answer
9. Hiring bar above candidate level
10. Hiring bar below candidate level

---

# Final Outcome

The system now:

- Supports both ICPs
- Produces adaptive questions
- Produces transcript-based scoring
- Generates negative gap values
- Uses real transcript quotes
- Differentiates strong vs weak candidates
- Completes full 3-turn interview pipeline