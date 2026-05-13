# Lesson 8: PeopleSoft-Inspired Row Security

## 1. Explain The Concept

Row security means a user should only see the student rows they are allowed to
see. In PeopleSoft, row security is a major security concept. This course uses a
simple PeopleSoft-inspired mock version so beginners can understand the idea.

This is not real PeopleSoft security administration. It is a training model.

## 2. Full Python And SQL Objects

Migration:

```text
migrations/001_add_row_security.sql
```

Shared Python tools:

```text
scripts/studentdb_tools.py
```

Security objects in SQLite:

```text
PS_SCRTY_OPR
PS_SCRTY_STUDENT
V_ROW_SECURITY_ACCESS
```

The second migration also adds student self-service operators:

```text
STUDENT_0001001
STUDENT_0001002
...
STUDENT_0001015
```

Each student operator can see only their own row.

## 3. Step By Step

1. `PS_SCRTY_OPR` stores mock operator IDs.
2. `PS_SCRTY_STUDENT` stores which `EMPLID` rows each operator can see.
3. `V_ROW_SECURITY_ACCESS` makes the access list easy to inspect.
4. `DatabaseDeps` reads the current operator from `STUDENTDB_OPRID`.
5. Query tools filter with `PS_SCRTY_STUDENT`.
6. The agent only receives rows that passed row security.

## 4. Important Functions

### `DatabaseDeps`

```python
@dataclass
class DatabaseDeps:
    db_path: Path = DB_PATH
    oprid: str = dataclass_field(
        default_factory=lambda: os.getenv("STUDENTDB_OPRID", "REGISTRAR_ALL").upper()
    )
```

### `get_operator_access`

Shows the current operator profile and allowed students.

### `find_students`

Filters student lookup through `PS_SCRTY_STUDENT`.

### `get_student_profile`

Returns no row if the current operator is not allowed to see that `EMPLID`.

## 5. Example User Question

```text
Show me Theo Lane
```

## 6. Example Assistant Response

With full access:

```bash
export STUDENTDB_OPRID=REGISTRAR_ALL
python final_project/studentdb_assistant.py "Show me Theo Lane"
```

The student is visible.

With Computer Science advisor access:

```bash
export STUDENTDB_OPRID=ADVISOR_COMP
python final_project/studentdb_assistant.py "Show me Theo Lane"
```

The student is not visible because Theo Lane is in Business Analytics, not
Computer Science.

## 7. Common Beginner Mistakes

- Thinking a prompt is enough for security. It is not.
- Filtering after data has already been sent to the model.
- Forgetting to apply row security to list queries.
- Treating "not found" and "not authorized" as the same thing in real systems.
  This course uses a simple "not found" response to avoid leaking which hidden
  records exist.

## 8. Practice Exercise

Run:

```bash
export STUDENTDB_OPRID=ADVISOR_LIMITED
python final_project/studentdb_assistant.py "Show me Zara Quinn"
python final_project/studentdb_assistant.py "Show me Orion Reed"
```

Explain why Zara is visible and Orion is not.

## 9. Capture A Transcript

Run:

```bash
python tests/capture_student_self_service_stdout.py
cat test_outputs/student_self_service_stdout.txt
```

This creates a reviewable stdout file showing student self-service access as
`STUDENT_0001005`.
