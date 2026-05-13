# StudentDB Assistant Exercises

## Exercise 1: Schema Inspection

Run:

```bash
python scripts/01_connect_sqlite.py
```

Question: Which views are designed for beginner-friendly student questions?

## Exercise 2: Pydantic Profile

Open `scripts/02_pydantic_models.py`.

Task: Change the hardcoded student from `0001005` to `0001004`. What is the
FERPA flag?

## Exercise 3: Student Classes

Open `scripts/03_query_tools.py`.

Task: Change `emplid = "0001006"` to `emplid = "0001012"` and list Orion Reed's
classes.

## Exercise 4: Positive Balances

Run:

```bash
python scripts/05_studentdb_cli.py "Which students owe money?"
```

Task: Confirm that negative balances are not included.

## Exercise 5: Incomplete Requirements

Run:

```bash
python final_project/studentdb_assistant.py "Which requirements are incomplete for 0001012?"
```

Task: Count the incomplete requirements.

## Exercise 6: Add A Route

Add support for:

```text
Which students have checklist items?
```

Use `V_STUDENT_CHECKLISTS`.

## Exercise 7: Explain The Safety Choice

In your own words, explain why the project formats exact balances in Python
instead of letting the AI model write the final number.

## Exercise 8: Test Row Security

Run:

```bash
export STUDENTDB_OPRID=ADVISOR_COMP
python final_project/studentdb_assistant.py "Show me Zara Quinn"
python final_project/studentdb_assistant.py "Show me Theo Lane"
```

Task: Explain why one student is visible and the other is not.

## Exercise 9: Test The MCP Server

Run:

```bash
python final_project/studentdb_mcp_server.py --list-tools
python final_project/studentdb_mcp_server.py --smoke-test
```

Then run:

```bash
STUDENTDB_OPRID=ADVISOR_COMP python final_project/studentdb_mcp_server.py --smoke-test
```

Task: Explain why the MCP server should wrap `studentdb_tools.py` instead of
creating a second set of SQL queries.
