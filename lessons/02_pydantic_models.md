# Lesson 2: Pydantic Models

## 1. Explain The Concept

SQL rows are loose dictionaries. Pydantic models give those rows a clear shape.
That makes assistant output easier to validate and easier to teach.

## 2. Full Python Script

Run:

```bash
python scripts/02_pydantic_models.py
```

## 3. Step By Step

- Query `V_STUDENT_360`.
- Use SQL aliases like `DISPLAY_NAME AS display_name`.
- Pass the row into `StudentProfile(**row)`.
- Pydantic checks the fields and types.

## 4. Important Functions

- `get_student_profile()`: returns `StudentProfile | None`.
- `money()`: formats balances while preserving signs.

## 5. Example User Question

```text
Show me a profile for Zara Quinn.
```

## 6. Example Assistant Response

```text
Zara Quinn is in B.S. Computer Science with GPA 3.91. FERPA flag is N.
```

## 7. Common Beginner Mistakes

- Forgetting SQL aliases.
- Making nullable fields required.
- Hiding important privacy fields like `FERPA_FLAG`.

## 8. Practice

Add `term_description` to the printed profile output.

## Row Security Note

Pydantic models validate the shape of rows after security filtering. A model
does not enforce security by itself. The SQL query must filter rows by the
current `STUDENTDB_OPRID` before creating a `StudentProfile`.
