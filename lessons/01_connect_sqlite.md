# Lesson 1: Connect To SQLite

## 1. Explain The Concept

SQLite is a database stored in one file. In this course, the file is:

```text
data/student_mock.db
```

Python can open this file with the built-in `sqlite3` module. Before using
Pydantic AI, prove that normal Python can read the data.

## 2. Full Python Script

Run:

```bash
python scripts/01_connect_sqlite.py
```

## 3. Step By Step

- `DB_PATH` points to the copied course database.
- `sqlite3.connect(DB_PATH)` opens the file.
- `row_factory = sqlite3.Row` lets Python turn rows into dictionaries.
- `sqlite_master` lists the real tables and views.
- `V_STUDENT_360` gives beginner-friendly student profile rows.

## 4. Important Functions

- `fetch_all()`: runs read-only SQL and returns dictionaries.
- `list_database_objects()`: lists tables and views.
- `sample_profiles()`: reads from `V_STUDENT_360`.

## 5. Example User Question

```text
What views are available for student data?
```

## 6. Example Assistant Response

```text
The student-facing views include V_STUDENT_360, V_STUDENT_CLASSES,
V_STUDENT_BALANCE, V_STUDENT_CHECKLISTS, V_STUDENT_HOLDS, and
V_STUDENT_REQUIREMENTS.
```

## 7. Common Beginner Mistakes

- Running the script from the wrong folder.
- Typing a table name that does not exist.
- Forgetting that views are queried like tables.

## 8. Practice

Change the profile query to show 10 rows instead of 5.

## Row Security Note

The database also includes PeopleSoft-inspired mock row-security objects:

- `PS_SCRTY_OPR`
- `PS_SCRTY_STUDENT`
- `V_ROW_SECURITY_ACCESS`

These objects decide which students an operator ID can see. Later lessons use
`STUDENTDB_OPRID` to filter student rows.
