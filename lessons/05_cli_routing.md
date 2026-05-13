# Lesson 5: CLI Routing

## 1. Explain The Concept

A command-line assistant needs to decide which database tool to run. This course
uses simple deterministic routing instead of asking the model to pick SQL.

## 2. Full Python Script

Run:

```bash
python scripts/05_studentdb_cli.py "Which students owe money?"
python scripts/05_studentdb_cli.py "Which students have holds?"
python scripts/05_studentdb_cli.py "Show me Theo Lane"
```

## 3. Step By Step

- Read the user question from `sys.argv`.
- Match phrases like `holds`, `owe`, or a student name.
- Run the matching read-only tool.
- Format exact values in Python.

## 4. Important Functions

- `route_question()`: chooses the route.
- `format_answer()`: formats exact facts.

## 5. Example User Question

```text
Which students owe money?
```

## 6. Example Assistant Response

```text
Students with positive balances:
- Orion Reed: $2,650
- Arlo Finch: $2,550
```

## 7. Common Beginner Mistakes

- Assuming every user phrase is supported.
- Using fuzzy AI routing before the safe routes work.
- Forgetting to preserve the negative sign on balances.

## 8. Practice

Add support for the phrase:

```text
Who has a balance due?
```

## Row Security Note

CLI routing must respect the current operator. For example:

```bash
export STUDENTDB_OPRID=ADVISOR_COMP
python scripts/05_studentdb_cli.py "Which students owe money?"
```

The answer should include only students visible to `ADVISOR_COMP`.
