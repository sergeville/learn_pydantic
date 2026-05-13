# Lesson 3: Read-Only Query Tools

## 1. Explain The Concept

A database tool is a Python function that answers one factual question. These
tools use read-only SQL and return Pydantic models.

## 2. Full Python Script

Run:

```bash
python scripts/03_query_tools.py
```

## 3. Step By Step

The script includes tools like:

- `get_student_profile(emplid)`
- `get_student_classes(emplid)`
- `get_student_balance(emplid)`
- `get_student_holds(emplid)`
- `find_students_with_holds()`
- `find_students_with_positive_balance()`

Each tool queries a real view from `student_mock.db`.

## 4. Important Functions

- `fetch_all()`: shared SQL helper.
- `get_student_classes()`: uses `V_STUDENT_CLASSES`.
- `find_students_with_positive_balance()`: uses `V_STUDENT_BALANCE WHERE BALANCE > 0`.

## 5. Example User Question

```text
Which students have holds?
```

## 6. Example Assistant Response

```text
Arlo Finch, Theo Lane, and Orion Reed have holds.
```

## 7. Common Beginner Mistakes

- Letting an AI model write arbitrary SQL.
- Forgetting parameterized SQL placeholders.
- Treating negative balances as money owed by the student.

## 8. Practice

Create a function named `get_student_checklists(emplid)` using
`V_STUDENT_CHECKLISTS`.

## Row Security Note

This is the lesson where row security matters most. Query tools should not read
all rows and then hide data later. They should filter inside SQL using
`PS_SCRTY_STUDENT` and the current `STUDENTDB_OPRID`.

Example idea:

```sql
AND EXISTS (
  SELECT 1
  FROM PS_SCRTY_STUDENT sec
  WHERE sec.OPRID = ?
    AND sec.EMPLID = V_STUDENT_360.EMPLID
)
```
