# Lesson 6: Final Project

## 1. Explain The Concept

The final project combines the pieces:

- SQLite connection
- Pydantic models
- read-only database tools
- command-line routing
- exact Python formatting
- optional Pydantic AI summary

## 2. Full Python Script

Run:

```bash
python final_project/studentdb_assistant.py "Show me Zara Quinn"
python final_project/studentdb_assistant.py "Which requirements are incomplete for 0001012?"
USE_AI_SUMMARY=1 python final_project/studentdb_assistant.py "Show me Theo Lane"
```

## 3. Step By Step

- `DatabaseDeps` stores the database path.
- Pydantic models describe profiles, classes, balances, holds, checklists, and
  requirements.
- Query functions read from the actual views.
- `create_student_success_report()` combines the tools.
- `route_question()` maps a question to a safe tool.
- `format_answer()` prints exact values.
- `USE_AI_SUMMARY=1` adds optional prose from Pydantic AI.

## 4. Important Functions

- `create_student_success_report()`
- `find_students_with_positive_balance()`
- `find_students_with_holds()`
- `find_students_by_gpa()`
- `guarded_ai_summary()`

## 5. Example User Question

```text
Generate a structured student success report for 0001012.
```

## 6. Example Assistant Response

```text
Student success report for Orion Reed (0001012)
- FERPA flag: N
- Program: Computer Science (AC)
- Balance: $2,650
- Holds: MFD Missing Final Document
```

## 7. Common Beginner Mistakes

- Confusing the final project with a chatbot server. This is a CLI assistant.
- Treating local AI summaries as authoritative.
- Ignoring `FERPA_FLAG = Y`.

## 8. Practice

Add a route for:

```text
Which students have checklist items?
```

## Row Security Note

The final project should never bypass `studentdb_tools.py` for student data.
Those shared tools apply the mock PeopleSoft-inspired row-security filter using
`STUDENTDB_OPRID`.
