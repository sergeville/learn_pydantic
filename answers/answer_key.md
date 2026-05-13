# Answer Key

## Exercise 1

The beginner-friendly views are:

- `V_STUDENT_360`
- `V_STUDENT_CLASSES`
- `V_STUDENT_BALANCE`
- `V_STUDENT_CHECKLISTS`
- `V_STUDENT_HOLDS`
- `V_STUDENT_REQUIREMENTS`

## Exercise 2

Arlo Finch (`0001004`) has:

```text
FERPA_FLAG = Y
```

In a real system, that should be treated as a privacy warning.

## Exercise 3

Orion Reed (`0001012`) is enrolled in:

- `CS 101`: Intro to Programming
- `MATH 120`: Calculus I

## Exercise 4

Students who owe money are represented by `BALANCE > 0`.

Zara Quinn has `-$250`, so Zara is not in the owes-money list. In this course's
account convention, a negative balance means a credit / institution owes the
student.

## Exercise 5

Orion Reed has three incomplete requirements in the current mock data:

- `BSCS-CAPSTONE`
- `BSCS-CSCORE`
- `BSCS-MATHREQ`

## Exercise 6

Suggested SQL:

```sql
SELECT *
FROM V_STUDENT_CHECKLISTS
ORDER BY EMPLID, DUE_DT
```

Suggested route condition:

```python
if "checklist" in normalized and "students" in normalized:
    ...
```

## Exercise 7

Exact facts such as balances, signs, holds, and FERPA flags should come from
SQL and deterministic Python formatting. A language model can summarize, but it
may omit or change important facts. That is risky for student-record-style data.

## Exercise 8

`ADVISOR_COMP` is seeded with access to students whose `ACAD_PROG` is `COMP`.

- Zara Quinn is visible because her academic program is Computer Science
  (`COMP`).
- Theo Lane is not visible because his academic program is Business Analytics
  (`BUSA`).

This is enforced by the mock row-security table `PS_SCRTY_STUDENT`, not by an AI
prompt.

## Exercise 9

The MCP server should wrap `studentdb_tools.py` because that file already
contains the read-only SQL, Pydantic models, balance formatting helper, and
row-security checks.

Creating a second SQL layer would be a maintainability and privacy risk:

- one tool might enforce `STUDENTDB_OPRID` while another forgets it
- balance rules could drift
- FERPA warnings could become inconsistent
- bugs would need to be fixed in two places

The correct design is:

```text
MCP tool -> studentdb_tools.py -> row-security-aware SQLite query
```
