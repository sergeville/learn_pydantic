# Lesson 9: Optional MCP Server

## 1. Explain The Concept In Simple Words

MCP means Model Context Protocol. It is a way for an AI client to call tools
from another program.

In this course, the MCP server lets another AI client call the same StudentDB
tools that the chatbot already uses.

That matters because the database rules stay in one place:

```text
AI client
  -> MCP server
  -> studentdb_tools.py
  -> row-security-aware SQLite queries
  -> student_mock.db
```

MCP is not the beginner starting point. It is an advanced integration step.
Start with SQLite, Pydantic models, Pydantic AI tools, the chatbot, and row
security first.

## 2. Show The Full Python Script

The full script is:

```text
final_project/studentdb_mcp_server.py
```

Run these commands from the course folder:

```bash
python final_project/studentdb_mcp_server.py --list-tools
python final_project/studentdb_mcp_server.py --smoke-test
```

To start the MCP server for a client:

```bash
python final_project/studentdb_mcp_server.py
```

By default, the server uses MCP over standard input/output. That is the normal
transport for local MCP clients.

If you installed the project as a package, use the console command instead:

```bash
studentdb-mcp
```

The example MCP client config is:

```text
mcp_config/studentdb_assistant_mcp.json
```

## 3. Explain The Script Step By Step

The script does these jobs:

1. Imports `FastMCP` from the `mcp` package.
2. Imports the existing StudentDB query functions from `scripts/studentdb_tools.py`.
3. Creates a `FastMCP` server named `StudentDB Assistant`.
4. Defines small MCP tools such as `get_student_profile`, `get_student_balance`,
   and `find_students_with_holds`.
5. Each MCP tool calls the existing safe database function.
6. The existing database function applies `STUDENTDB_OPRID` row security.
7. The MCP tool returns normal JSON-friendly Python dictionaries.
8. The script can run a smoke test before you connect it to an AI client.
9. The script can start the MCP server when no test flag is provided.

The important design choice is that the MCP server does not write new SQL for
every tool. It reuses the course tools. That keeps security and behavior
consistent.

## 4. Explain What Each Important Function Does

`deps()`

Creates a `DatabaseDeps` object. This tells the tools which database to use and
which operator ID is active.

`as_jsonable(value)`

Converts Pydantic models into normal dictionaries so MCP clients can read the
result.

`resolve_student_ref(student_ref)`

Finds a visible student by EMPLID or name. If row security hides the student,
the function returns nothing.

`inspect_schema()`

Returns the actual tables and views in `student_mock.db`.

`inspect_row_security()`

Shows the current `STUDENTDB_OPRID`, its access profile, and the visible
students.

`get_student_balance(student_ref)`

Returns the student balance and includes the rule:

```text
BALANCE > 0 means the student owes money.
BALANCE < 0 means the student has a credit.
```

`create_student_success_report(student_ref)`

Builds an advisor-ready structured report by combining profile, classes,
balance, holds, checklist items, requirements, and financial aid.

`smoke_test()`

Runs a deterministic local check without requiring an MCP client.

`main()`

Handles `--list-tools`, `--smoke-test`, or starts the MCP server.

## 5. Show An Example User Question

In an MCP-compatible AI client, the user can ask:

```text
Tell me about Zara Quinn.
```

The AI client can choose the MCP tool:

```text
create_student_success_report
```

The MCP server queries the database and returns structured evidence.

## 6. Show An Example Assistant Response

Example response:

```text
Zara Quinn is an active Computer Science student in the B.S. Computer Science
plan. Her GPA is 3.91. She has a -$250 balance, which means she has a credit.
No holds are listed. Several degree requirements are still marked Not
Satisfied.
```

The exact facts come from the SQLite database. The wording comes from the AI
client.

## 7. Explain Common Beginner Mistakes

Mistake: starting with MCP before understanding the database.

Better: learn SQLite and the query tools first.

Mistake: writing new SQL inside the MCP server.

Better: wrap `studentdb_tools.py` so all tools share the same row-security
logic.

Mistake: assuming MCP replaces Pydantic AI.

Better: treat MCP as an integration layer. Pydantic AI is still useful for
building the Python chatbot and structured agent behavior.

Mistake: exposing unrestricted student data.

Better: always use `STUDENTDB_OPRID` and row-security-aware tools.

Mistake: letting the LLM guess.

Better: the LLM should call MCP tools for facts and say when the answer is not
found.

## 8. Give A Small Practice Exercise

1. Run:

```bash
python final_project/studentdb_mcp_server.py --smoke-test
```

2. Then test row security:

```bash
STUDENTDB_OPRID=ADVISOR_COMP python final_project/studentdb_mcp_server.py --smoke-test
```

3. Compare the visible students.

4. Explain why Theo Lane is hidden from `ADVISOR_COMP`.

5. Add one new MCP tool that wraps an existing function in `studentdb_tools.py`.

Do not add raw SQL unless there is no existing shared tool to reuse.
