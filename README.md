# StudentDB Assistant Course

Learn Pydantic AI by building a read-only AI assistant over a real SQLite mock
student information system.

## Start Here If You Are New

Open this file first. Then follow the course in this order:

1. Read `SYLLABUS.md`
2. Read `lessons/01_connect_sqlite.md`
3. Run `python scripts/01_connect_sqlite.py`
4. Continue through lessons `02` to `08` in order
5. Run the final project after you understand the lesson scripts
6. Read optional `lessons/09_mcp_server.md` after the chatbot works

Quick start from the parent project environment:

```bash
cd ~/Dev/pscs_inspired_mock/studentdb_assistant_course
source ../.venv/bin/activate
python tests/validate_course.py
python scripts/01_connect_sqlite.py
```

Do not start with the chatbot first. Start with the SQLite lesson so the AI
assistant feels like normal Python code, not magic.

## What This Course Contains

- `data/student_mock.db`: the SQLite database used by every lesson
- `migrations/001_add_row_security.sql`: PeopleSoft-inspired mock row security
- `lessons/`: classroom notes for each module
- `scripts/`: runnable Python scripts for each lesson
- `exercises/`: practice tasks
- `answers/`: answer key and suggested solutions
- `final_project/`: complete StudentDB Assistant
- `final_project/studentdb_mcp_server.py`: optional MCP server extension
- `mcp_config/`: example MCP client configuration
- `tests/validate_course.py`: quick validation script

## Setup

For course development from this folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Install As A Package On macOS Or Linux

This project can also be installed as a normal Python package. That gives you
terminal commands instead of requiring `python final_project/...` paths.

From a fresh machine:

```bash
git clone https://github.com/sergeville/learn_pydantic.git
cd learn_pydantic
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

For editable course development:

```bash
python -m pip install -e .
```

Installed commands:

```bash
studentdb-assistant "Show me Zara Quinn"
studentdb-chat
studentdb-mcp --list-tools
studentdb-mcp --smoke-test
```

The package includes the mock SQLite database at install time. To point the
installed commands at a different copy of the database:

```bash
export STUDENTDB_DB_PATH=/path/to/student_mock.db
```

## PeopleSoft-Inspired Row Security

The course now includes mock row security. It is not real PeopleSoft security,
but it teaches the same core idea: the current operator ID (`OPRID`) controls
which student rows can be seen.

Security objects added to `data/student_mock.db`:

- `PS_SCRTY_OPR`: mock operator/security profile table
- `PS_SCRTY_STUDENT`: mock operator-to-student access table
- `V_ROW_SECURITY_ACCESS`: readable access view

Available training operators:

```text
REGISTRAR_ALL     sees all students
ADVISOR_COMP      sees Computer Science students only
ADVISOR_BUSA      sees Business Analytics students only
ADVISOR_LIMITED   sees Zara Quinn and Theo Lane only
NO_ACCESS         sees no student rows
STUDENT_0001005   student self-service login for Zara Quinn only
```

Choose an operator with:

```bash
export STUDENTDB_OPRID=ADVISOR_COMP
python final_project/studentdb_assistant.py "Show me Zara Quinn"
python final_project/studentdb_assistant.py "Show me Theo Lane"
```

With `ADVISOR_COMP`, Zara is visible because she is in Computer Science. Theo is
not visible because he is in Business Analytics. This filtering is enforced in
the SQLite query tools, not just in the prompt.

To capture a full student self-service stdout transcript:

```bash
python tests/capture_student_self_service_stdout.py
cat test_outputs/student_self_service_stdout.txt
```

To record a full student walkthrough as Markdown:

```bash
python tests/record_course_walkthrough.py
open course_runs/student_course_walkthrough.md
```

The walkthrough recorder captures each command, stdout, stderr, and exit code.
It also creates `course_runs/images/` for screenshots if a future lesson needs
visual evidence.

For local Ollama summaries:

```bash
ollama serve
ollama pull llama3.2
export PYDANTIC_AI_MODEL="ollama:llama3.2"
export OLLAMA_BASE_URL="http://localhost:11434/v1"
```

## Run The Lessons

```bash
python scripts/01_connect_sqlite.py
python scripts/02_pydantic_models.py
python scripts/03_query_tools.py
python scripts/04_pydantic_ai_summary.py
python scripts/05_studentdb_cli.py "Which students owe money?"
```

Read `lessons/08_row_security.md` after the conversational-agent lesson.
Read optional `lessons/09_mcp_server.md` after the chatbot works.

## Run The Final Project

```bash
python final_project/studentdb_assistant.py "Show me Zara Quinn"
python final_project/studentdb_assistant.py "Which students have holds?"
python final_project/studentdb_assistant.py "Which requirements are incomplete for 0001012?"
python final_project/studentdb_assistant.py "Which students owe money?"
```

Optional AI summary:

```bash
USE_AI_SUMMARY=1 python final_project/studentdb_assistant.py "Show me Theo Lane"
```

## Run The Conversational Agent

```bash
python final_project/conversational_studentdb_agent.py
```

Then ask questions until you type `exit`:

```text
Tell me about student 0001005
What classes is this student taking?
Does this student owe money?
Summarize this student for an advisor.
exit
```

The conversational script defaults to safe local mode because small Ollama
models can be unreliable at strict Pydantic AI tool-calling. To try real
Pydantic AI tool mode with a tool-capable model:

```bash
STUDENTDB_AGENT_MODE=tools python final_project/conversational_studentdb_agent.py
```

## Run The Optional MCP Server

MCP is useful when you want another MCP-compatible AI client to call the same
StudentDB tools. It should come after the basic Python, Pydantic, Pydantic AI,
chatbot, and row-security lessons.

First run the deterministic smoke test:

```bash
python final_project/studentdb_mcp_server.py --smoke-test
```

List the exposed MCP tools:

```bash
python final_project/studentdb_mcp_server.py --list-tools
```

Start the MCP server over standard input/output:

```bash
python final_project/studentdb_mcp_server.py
```

Use `mcp_config/studentdb_assistant_mcp.json` as a starting point for MCP
clients that accept JSON server configuration. Change `STUDENTDB_OPRID` in the
config to test row security.

After installing the package, the MCP server command is:

```bash
studentdb-mcp
```

## Validate The Course

```bash
python tests/validate_course.py
```

## Safety Rule

This course uses read-only SQL. The assistant should query facts from the
database, format exact values in Python, and only use AI for optional
summaries. Student/account facts should not depend on a model guessing.

Row security is also enforced in the database tools. Do not bypass
`studentdb_tools.py` with raw unfiltered queries in assistant code.

The MCP server follows the same rule. It wraps `studentdb_tools.py`; it does
not create a second query system.
