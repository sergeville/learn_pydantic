# StudentDB Assistant Course Walkthrough

Generated: 2026-05-13T15:12:30

This file records the actions of a new student taking the course.
Each action includes the command, stdout, stderr when present, and exit code.

## Images

No images were needed for this terminal-based walkthrough.
If screenshots are added later, store them under `course_runs/images/` and link them here.

## Open the course README

A new student starts by reading the README start-here instructions.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python -c &quot;from pathlib import Path; print(Path(&#x27;README.md&#x27;).read_text()[:2200])&quot;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code># StudentDB Assistant Course

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
cd /Users/sergevilleneuve/Downloads/pscs_inspired_mock/studentdb_assistant_course
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
studentdb-assistant &quot;Show me Zara Quinn&quot;
studentdb-chat
studentd</code></pre>
</div>

## Validate the course package

Before learning, confirm the database, scripts, row security, and chatbot smoke tests pass.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python tests/validate_course.py</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Course validation passed.</code></pre>
</div>

## Lesson 1: Connect to SQLite

Run the first script to inspect the real database objects and sample student rows.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python scripts/01_connect_sqlite.py</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Database: /Users/sergevilleneuve/Downloads/pscs_inspired_mock/studentdb_assistant_course/data/student_mock.db

Tables and views:
- table: CS_AA_REQUIREMENT_STATUS
- table: CS_CC_CHECKLIST
- table: CS_CC_PERSON
- table: CS_CC_SERVICE_INDICATOR
- table: CS_FA_AWARD
- table: CS_SF_ACCOUNT_ITEM
- table: CS_SR_ACAD_PLAN
- table: CS_SR_ACAD_PROGRAM
- table: CS_SR_CLASS_ENROLLMENT
- table: CS_SR_CLASS_SCHEDULE
- table: CS_SR_COURSE_CATALOG
- table: CS_SR_TERM_ENROLLMENT
- table: PS_SCRTY_OPR
- table: PS_SCRTY_STUDENT
- view: V_ROW_SECURITY_ACCESS
- view: V_STUDENT_360
- view: V_STUDENT_BALANCE
- view: V_STUDENT_CHECKLISTS
- view: V_STUDENT_CLASSES
- view: V_STUDENT_HOLDS
- view: V_STUDENT_REQUIREMENTS

Sample V_STUDENT_360 rows:
{&#x27;EMPLID&#x27;: &#x27;0001001&#x27;, &#x27;DISPLAY_NAME&#x27;: &#x27;Nova Hart&#x27;, &#x27;FERPA_FLAG&#x27;: &#x27;N&#x27;, &#x27;PROG_DESCR&#x27;: &#x27;Computer Science&#x27;, &#x27;PLAN_DESCR&#x27;: &#x27;B.S. Computer Science&#x27;, &#x27;CUM_GPA&#x27;: 3.62, &#x27;PROG_STATUS&#x27;: &#x27;AC&#x27;}
{&#x27;EMPLID&#x27;: &#x27;0001002&#x27;, &#x27;DISPLAY_NAME&#x27;: &#x27;Kai Rivers&#x27;, &#x27;FERPA_FLAG&#x27;: &#x27;N&#x27;, &#x27;PROG_DESCR&#x27;: &#x27;Mathematics&#x27;, &#x27;PLAN_DESCR&#x27;: &#x27;B.S. Mathematics&#x27;, &#x27;CUM_GPA&#x27;: 3.78, &#x27;PROG_STATUS&#x27;: &#x27;AC&#x27;}
{&#x27;EMPLID&#x27;: &#x27;0001003&#x27;, &#x27;DISPLAY_NAME&#x27;: &#x27;Mina Sol&#x27;, &#x27;FERPA_FLAG&#x27;: &#x27;N&#x27;, &#x27;PROG_DESCR&#x27;: &#x27;Biology&#x27;, &#x27;PLAN_DESCR&#x27;: &#x27;B.S. Biology&#x27;, &#x27;CUM_GPA&#x27;: 3.41, &#x27;PROG_STATUS&#x27;: &#x27;AC&#x27;}
{&#x27;EMPLID&#x27;: &#x27;0001004&#x27;, &#x27;DISPLAY_NAME&#x27;: &#x27;Arlo Finch&#x27;, &#x27;FERPA_FLAG&#x27;: &#x27;Y&#x27;, &#x27;PROG_DESCR&#x27;: &#x27;Business Analytics&#x27;, &#x27;PLAN_DESCR&#x27;: &#x27;B.S. Business Analytics&#x27;, &#x27;CUM_GPA&#x27;: 3.25, &#x27;PROG_STATUS&#x27;: &#x27;AC&#x27;}
{&#x27;EMPLID&#x27;: &#x27;0001005&#x27;, &#x27;DISPLAY_NAME&#x27;: &#x27;Zara Quinn&#x27;, &#x27;FERPA_FLAG&#x27;: &#x27;N&#x27;, &#x27;PROG_DESCR&#x27;: &#x27;Computer Science&#x27;, &#x27;PLAN_DESCR&#x27;: &#x27;B.S. Computer Science&#x27;, &#x27;CUM_GPA&#x27;: 3.91, &#x27;PROG_STATUS&#x27;: &#x27;AC&#x27;}</code></pre>
</div>

## Lesson 2: Pydantic models

Convert a real SQLite row into a Pydantic model and print a beginner-friendly answer.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python scripts/02_pydantic_models.py</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Pydantic model:
{
  &quot;emplid&quot;: &quot;0001005&quot;,
  &quot;display_name&quot;: &quot;Zara Quinn&quot;,
  &quot;ferpa_flag&quot;: &quot;N&quot;,
  &quot;academic_career&quot;: &quot;UGRD&quot;,
  &quot;program_code&quot;: &quot;COMP&quot;,
  &quot;program&quot;: &quot;Computer Science&quot;,
  &quot;plan_code&quot;: &quot;BSCS&quot;,
  &quot;plan&quot;: &quot;B.S. Computer Science&quot;,
  &quot;program_status&quot;: &quot;AC&quot;,
  &quot;gpa&quot;: 3.91,
  &quot;cumulative_units&quot;: 50,
  &quot;term&quot;: &quot;2261&quot;,
  &quot;term_description&quot;: &quot;Spring 2026&quot;,
  &quot;enrollment_status&quot;: &quot;E&quot;
}

Beginner-friendly answer:
Zara Quinn is in B.S. Computer Science with GPA 3.91. FERPA flag is N.
Balance for term 2261: -$250</code></pre>
</div>

## Lesson 3: Query tools

Run several read-only student database tools.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python scripts/03_query_tools.py</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Profile:
emplid=&#x27;0001006&#x27; display_name=&#x27;Theo Lane&#x27; ferpa_flag=&#x27;N&#x27; academic_career=&#x27;UGRD&#x27; program_code=&#x27;BUSA&#x27; program=&#x27;Business Analytics&#x27; plan_code=&#x27;BSBA&#x27; plan=&#x27;B.S. Business Analytics&#x27; program_status=&#x27;AC&#x27; gpa=2.98 cumulative_units=68 term=&#x27;2261&#x27; term_description=&#x27;Spring 2026&#x27; enrollment_status=&#x27;E&#x27;

Classes:
emplid=&#x27;0001006&#x27; display_name=&#x27;Theo Lane&#x27; term=&#x27;2251&#x27; class_number=&#x27;12352&#x27; subject=&#x27;BUS&#x27; catalog_number=&#x27;150&#x27; course=&#x27;Business Fundamentals&#x27; enrollment_status=&#x27;D&#x27; units=3 grade=&#x27;B-&#x27;
emplid=&#x27;0001006&#x27; display_name=&#x27;Theo Lane&#x27; term=&#x27;2261&#x27; class_number=&#x27;12353&#x27; subject=&#x27;BUS&#x27; catalog_number=&#x27;310&#x27; course=&#x27;Analytics for Decision Making&#x27; enrollment_status=&#x27;E&#x27; units=3 grade=None

Balance:
$1,750

Holds for student:
emplid=&#x27;0001006&#x27; display_name=&#x27;Theo Lane&#x27; code=&#x27;ADV&#x27; reason=&#x27;Advising Required&#x27; start_term=&#x27;2261&#x27; impact=&#x27;Enrollment&#x27;

All students with holds:
Arlo Finch: FIN / Past Due Balance
Theo Lane: ADV / Advising Required
Orion Reed: MFD / Missing Final Document

Students with positive balances:
Orion Reed: $2,650
Arlo Finch: $2,550
Nia Bloom: $2,250
Rumi Cole: $1,850
Theo Lane: $1,750
Ezra Cove: $1,650
Leo Vale: $1,450
Mina Sol: $1,250
Juno Park: $1,250
Nova Hart: $1,050
Luna Gray: $150
Ivy Moss: $50</code></pre>
</div>

## Lesson 4: Optional Pydantic AI summary

This lesson needs a local Ollama server and a model that can answer from evidence.

Note: Skipped by default in the recorder so the walkthrough remains deterministic. Run RUN_AI_ACTIONS=1 python tests/record_course_walkthrough.py to include it.

No command was run for this action.

## Lesson 5: CLI routing

Ask a normal-language question without writing SQL.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python scripts/05_studentdb_cli.py &#x27;Which students owe money?&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Students with positive balances:
- Orion Reed (0001012): $2,650
- Arlo Finch (0001004): $2,550
- Nia Bloom (0001009): $2,250
- Rumi Cole (0001014): $1,850
- Theo Lane (0001006): $1,750
- Ezra Cove (0001010): $1,650
- Leo Vale (0001008): $1,450
- Mina Sol (0001003): $1,250
- Juno Park (0001015): $1,250
- Nova Hart (0001001): $1,050
- Luna Gray (0001011): $150
- Ivy Moss (0001007): $50</code></pre>
</div>

## Final project: student report

Ask for a student success report by name.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_assistant.py &#x27;Show me Zara Quinn&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Student success report for Zara Quinn (0001005)
- FERPA flag: N
- Program: Computer Science (AC)
- Plan: B.S. Computer Science
- GPA: 3.91
- Balance: -$250

Holds:
- No holds listed.

Incomplete requirements:
- BSCS-CAPSTONE: Complete AI Systems Lab or capstone
- BSCS-CSCORE: Complete CS core
- BSCS-MATHREQ: Complete math requirement</code></pre>
</div>

## Final project: incomplete requirements

Ask for incomplete requirements by EMPLID.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_assistant.py &#x27;Which requirements are incomplete for 0001012?&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Incomplete requirements:
- BSCS-CAPSTONE: Complete AI Systems Lab or capstone (0/4 units)
- BSCS-CSCORE: Complete CS core (0/28 units)
- BSCS-MATHREQ: Complete math requirement (0/12 units)</code></pre>
</div>

## Row security: advisor can see assigned program

ADVISOR_COMP can see Computer Science students such as Zara Quinn.

<div style="border-left: 4px solid #2563eb; background: #eff6ff; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">Environment overrides</div>
  <pre style="background: #0f172a; color: #dbeafe; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>STUDENTDB_OPRID=ADVISOR_COMP</code></pre>
</div>

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_assistant.py &#x27;Show me Zara Quinn&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Student success report for Zara Quinn (0001005)
- FERPA flag: N
- Program: Computer Science (AC)
- Plan: B.S. Computer Science
- GPA: 3.91
- Balance: -$250

Holds:
- No holds listed.

Incomplete requirements:
- BSCS-CAPSTONE: Complete AI Systems Lab or capstone
- BSCS-CSCORE: Complete CS core
- BSCS-MATHREQ: Complete math requirement</code></pre>
</div>

## Row security: advisor cannot see other program

ADVISOR_COMP cannot see Business Analytics student Theo Lane.

<div style="border-left: 4px solid #2563eb; background: #eff6ff; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">Environment overrides</div>
  <pre style="background: #0f172a; color: #dbeafe; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>STUDENTDB_OPRID=ADVISOR_COMP</code></pre>
</div>

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_assistant.py &#x27;Show me Theo Lane&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>No matching student was found for: Show me Theo Lane</code></pre>
</div>

## Student self-service: own row only

STUDENT_0001005 can see Zara Quinn.

<div style="border-left: 4px solid #2563eb; background: #eff6ff; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">Environment overrides</div>
  <pre style="background: #0f172a; color: #dbeafe; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>STUDENTDB_OPRID=STUDENT_0001005</code></pre>
</div>

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_assistant.py &#x27;Show me Zara Quinn&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Student success report for Zara Quinn (0001005)
- FERPA flag: N
- Program: Computer Science (AC)
- Plan: B.S. Computer Science
- GPA: 3.91
- Balance: -$250

Holds:
- No holds listed.

Incomplete requirements:
- BSCS-CAPSTONE: Complete AI Systems Lab or capstone
- BSCS-CSCORE: Complete CS core
- BSCS-MATHREQ: Complete math requirement</code></pre>
</div>

## Student self-service: another student hidden

STUDENT_0001005 cannot see Theo Lane.

<div style="border-left: 4px solid #2563eb; background: #eff6ff; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">Environment overrides</div>
  <pre style="background: #0f172a; color: #dbeafe; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>STUDENTDB_OPRID=STUDENT_0001005</code></pre>
</div>

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_assistant.py &#x27;Show me Theo Lane&#x27;</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>No matching student was found for: Show me Theo Lane</code></pre>
</div>

## Conversational agent walkthrough

Run the terminal chatbot with scripted input and capture the whole conversation.

<div style="border-left: 4px solid #2563eb; background: #eff6ff; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">Environment overrides</div>
  <pre style="background: #0f172a; color: #dbeafe; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>STUDENTDB_OPRID=STUDENT_0001005</code></pre>
</div>

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/conversational_studentdb_agent.py &lt;&lt;&#x27;STDIN&#x27;
Tell me about student 0001005
What classes is this student taking?
Does this student owe money?
Show me Theo Lane
exit
STDIN</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>StudentDB Conversational Agent
Type a question, or type exit to quit.
Example: Tell me about student 0001005
Mode: safe
Set STUDENTDB_AGENT_MODE=tools to try Pydantic AI tool-calling with a tool-capable model.

User: 
Agent: Advisor summary for Zara Quinn (0001005):
- Program: Computer Science
- GPA: 3.91
- Balance: -$250
- Holds: 0
- Incomplete requirements: 3
Tools used: create_student_success_report_tool

User: 
Agent: Zara Quinn is enrolled in:
- CS 101: Intro to Programming
- CS 220: Data Structures
- CS 330: Databases and Knowledge Graphs
- CS 410: AI Systems Lab
Tools used: get_student_classes_tool

User: 
Agent: No. Zara Quinn has a credit balance of -$250.
Tools used: get_student_balance_tool

User: 
Agent: I could not find that answer in the database. Try naming a student or asking about holds, balances, GPA, checklist items, or active students.

User: Agent: Goodbye.</code></pre>
</div>

## Student self-service stdout capture

Run the focused transcript generator that writes a plain stdout file.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python tests/capture_student_self_service_stdout.py</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>Wrote transcript to /Users/sergevilleneuve/Downloads/pscs_inspired_mock/studentdb_assistant_course/test_outputs/student_self_service_stdout.txt</code></pre>
</div>

## Lesson 9: MCP server tool list

List the MCP tools exposed for compatible AI clients.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_mcp_server.py --list-tools</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>inspect_schema
inspect_row_security
search_students
list_active_students
get_student_profile
get_student_classes
get_student_balance
get_student_holds
get_student_checklists
get_student_requirements
get_student_financial_aid
find_students_with_holds
find_students_with_positive_balances
find_students_by_gpa
find_students_with_incomplete_requirements
find_students_with_checklist_items
find_academic_risk_students
create_student_success_report</code></pre>
</div>

## Lesson 9: MCP server smoke test

Run the deterministic MCP smoke test without starting a blocking server process.

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_mcp_server.py --smoke-test</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>{
  &quot;server&quot;: &quot;StudentDB Assistant MCP&quot;,
  &quot;oprid&quot;: &quot;REGISTRAR_ALL&quot;,
  &quot;tool_count&quot;: 18,
  &quot;tools&quot;: [
    &quot;inspect_schema&quot;,
    &quot;inspect_row_security&quot;,
    &quot;search_students&quot;,
    &quot;list_active_students&quot;,
    &quot;get_student_profile&quot;,
    &quot;get_student_classes&quot;,
    &quot;get_student_balance&quot;,
    &quot;get_student_holds&quot;,
    &quot;get_student_checklists&quot;,
    &quot;get_student_requirements&quot;,
    &quot;get_student_financial_aid&quot;,
    &quot;find_students_with_holds&quot;,
    &quot;find_students_with_positive_balances&quot;,
    &quot;find_students_by_gpa&quot;,
    &quot;find_students_with_incomplete_requirements&quot;,
    &quot;find_students_with_checklist_items&quot;,
    &quot;find_academic_risk_students&quot;,
    &quot;create_student_success_report&quot;
  ],
  &quot;row_security&quot;: {
    &quot;operator&quot;: {
      &quot;OPRID&quot;: &quot;REGISTRAR_ALL&quot;,
      &quot;DESCR&quot;: &quot;Registrar super user for training&quot;,
      &quot;ACCESS_PROFILE&quot;: &quot;All students&quot;
    },
    &quot;allowed_students&quot;: [
      {
        &quot;EMPLID&quot;: &quot;0001001&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Nova Hart&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001002&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Kai Rivers&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001003&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Mina Sol&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001004&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Arlo Finch&quot;,
        &quot;FERPA_FLAG&quot;: &quot;Y&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001005&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Zara Quinn&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001006&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Theo Lane&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001007&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Ivy Moss&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001008&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Leo Vale&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001009&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Nia Bloom&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001010&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Ezra Cove&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001011&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Luna Gray&quot;,
        &quot;FERPA_FLAG&quot;: &quot;Y&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001012&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Orion Reed&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001013&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Sage Patel&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001014&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Rumi Cole&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001015&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Juno Park&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Registrar training access&quot;
      }
    ],
    &quot;allowed_count&quot;: 15
  },
  &quot;zara_profile&quot;: {
    &quot;found&quot;: true,
    &quot;profile&quot;: {
      &quot;emplid&quot;: &quot;0001005&quot;,
      &quot;display_name&quot;: &quot;Zara Quinn&quot;,
      &quot;ferpa_flag&quot;: &quot;N&quot;,
      &quot;academic_career&quot;: &quot;UGRD&quot;,
      &quot;program_code&quot;: &quot;COMP&quot;,
      &quot;program&quot;: &quot;Computer Science&quot;,
      &quot;plan_code&quot;: &quot;BSCS&quot;,
      &quot;plan&quot;: &quot;B.S. Computer Science&quot;,
      &quot;program_status&quot;: &quot;AC&quot;,
      &quot;gpa&quot;: 3.91,
      &quot;cumulative_units&quot;: 50,
      &quot;term&quot;: &quot;2261&quot;,
      &quot;term_description&quot;: &quot;Spring 2026&quot;,
      &quot;enrollment_status&quot;: &quot;E&quot;
    }
  },
  &quot;positive_balances&quot;: {
    &quot;balances&quot;: [
      {
        &quot;emplid&quot;: &quot;0001012&quot;,
        &quot;display_name&quot;: &quot;Orion Reed&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 2650.0,
        &quot;formatted_balance&quot;: &quot;$2,650&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001004&quot;,
        &quot;display_name&quot;: &quot;Arlo Finch&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 2550.0,
        &quot;formatted_balance&quot;: &quot;$2,550&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001009&quot;,
        &quot;display_name&quot;: &quot;Nia Bloom&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 2250.0,
        &quot;formatted_balance&quot;: &quot;$2,250&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001014&quot;,
        &quot;display_name&quot;: &quot;Rumi Cole&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1850.0,
        &quot;formatted_balance&quot;: &quot;$1,850&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001006&quot;,
        &quot;display_name&quot;: &quot;Theo Lane&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1750.0,
        &quot;formatted_balance&quot;: &quot;$1,750&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001010&quot;,
        &quot;display_name&quot;: &quot;Ezra Cove&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1650.0,
        &quot;formatted_balance&quot;: &quot;$1,650&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001008&quot;,
        &quot;display_name&quot;: &quot;Leo Vale&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1450.0,
        &quot;formatted_balance&quot;: &quot;$1,450&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001003&quot;,
        &quot;display_name&quot;: &quot;Mina Sol&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1250.0,
        &quot;formatted_balance&quot;: &quot;$1,250&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001015&quot;,
        &quot;display_name&quot;: &quot;Juno Park&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1250.0,
        &quot;formatted_balance&quot;: &quot;$1,250&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001001&quot;,
        &quot;display_name&quot;: &quot;Nova Hart&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1050.0,
        &quot;formatted_balance&quot;: &quot;$1,050&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001011&quot;,
        &quot;display_name&quot;: &quot;Luna Gray&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 150.0,
        &quot;formatted_balance&quot;: &quot;$150&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001007&quot;,
        &quot;display_name&quot;: &quot;Ivy Moss&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 50.0,
        &quot;formatted_balance&quot;: &quot;$50&quot;
      }
    ],
    &quot;balance_rule&quot;: &quot;BALANCE &gt; 0 means the student owes money. BALANCE &lt; 0 means the student has a credit.&quot;
  }
}</code></pre>
</div>

## Lesson 9: MCP row security smoke test

Show that the MCP server still respects STUDENTDB_OPRID row security.

<div style="border-left: 4px solid #2563eb; background: #eff6ff; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #2563eb; margin-bottom: 0.5rem;">Environment overrides</div>
  <pre style="background: #0f172a; color: #dbeafe; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>STUDENTDB_OPRID=ADVISOR_COMP</code></pre>
</div>

<div style="border-left: 4px solid #16a34a; background: #f0fdf4; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #16a34a; margin-bottom: 0.5rem;">Executed command</div>
  <pre style="background: #052e16; color: #dcfce7; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>/Users/sergevilleneuve/Downloads/pscs_inspired_mock/.venv/bin/python final_project/studentdb_mcp_server.py --smoke-test</code></pre>
</div>

Exit code: <span style="color: #16a34a; font-weight: 700;">0</span>

<div style="border-left: 4px solid #475569; background: #f8fafc; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">
  <div style="font-weight: 700; color: #475569; margin-bottom: 0.5rem;">Stdout</div>
  <pre style="background: #111827; color: #e5e7eb; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>{
  &quot;server&quot;: &quot;StudentDB Assistant MCP&quot;,
  &quot;oprid&quot;: &quot;ADVISOR_COMP&quot;,
  &quot;tool_count&quot;: 18,
  &quot;tools&quot;: [
    &quot;inspect_schema&quot;,
    &quot;inspect_row_security&quot;,
    &quot;search_students&quot;,
    &quot;list_active_students&quot;,
    &quot;get_student_profile&quot;,
    &quot;get_student_classes&quot;,
    &quot;get_student_balance&quot;,
    &quot;get_student_holds&quot;,
    &quot;get_student_checklists&quot;,
    &quot;get_student_requirements&quot;,
    &quot;get_student_financial_aid&quot;,
    &quot;find_students_with_holds&quot;,
    &quot;find_students_with_positive_balances&quot;,
    &quot;find_students_by_gpa&quot;,
    &quot;find_students_with_incomplete_requirements&quot;,
    &quot;find_students_with_checklist_items&quot;,
    &quot;find_academic_risk_students&quot;,
    &quot;create_student_success_report&quot;
  ],
  &quot;row_security&quot;: {
    &quot;operator&quot;: {
      &quot;OPRID&quot;: &quot;ADVISOR_COMP&quot;,
      &quot;DESCR&quot;: &quot;Computer Science advisor for training&quot;,
      &quot;ACCESS_PROFILE&quot;: &quot;Computer Science students&quot;
    },
    &quot;allowed_students&quot;: [
      {
        &quot;EMPLID&quot;: &quot;0001001&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Nova Hart&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Program advisor access: COMP&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001005&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Zara Quinn&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Program advisor access: COMP&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001008&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Leo Vale&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Program advisor access: COMP&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001012&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Orion Reed&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Program advisor access: COMP&quot;
      },
      {
        &quot;EMPLID&quot;: &quot;0001013&quot;,
        &quot;DISPLAY_NAME&quot;: &quot;Sage Patel&quot;,
        &quot;FERPA_FLAG&quot;: &quot;N&quot;,
        &quot;ACCESS_REASON&quot;: &quot;Program advisor access: COMP&quot;
      }
    ],
    &quot;allowed_count&quot;: 5
  },
  &quot;zara_profile&quot;: {
    &quot;found&quot;: true,
    &quot;profile&quot;: {
      &quot;emplid&quot;: &quot;0001005&quot;,
      &quot;display_name&quot;: &quot;Zara Quinn&quot;,
      &quot;ferpa_flag&quot;: &quot;N&quot;,
      &quot;academic_career&quot;: &quot;UGRD&quot;,
      &quot;program_code&quot;: &quot;COMP&quot;,
      &quot;program&quot;: &quot;Computer Science&quot;,
      &quot;plan_code&quot;: &quot;BSCS&quot;,
      &quot;plan&quot;: &quot;B.S. Computer Science&quot;,
      &quot;program_status&quot;: &quot;AC&quot;,
      &quot;gpa&quot;: 3.91,
      &quot;cumulative_units&quot;: 50,
      &quot;term&quot;: &quot;2261&quot;,
      &quot;term_description&quot;: &quot;Spring 2026&quot;,
      &quot;enrollment_status&quot;: &quot;E&quot;
    }
  },
  &quot;positive_balances&quot;: {
    &quot;balances&quot;: [
      {
        &quot;emplid&quot;: &quot;0001012&quot;,
        &quot;display_name&quot;: &quot;Orion Reed&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 2650.0,
        &quot;formatted_balance&quot;: &quot;$2,650&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001008&quot;,
        &quot;display_name&quot;: &quot;Leo Vale&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1450.0,
        &quot;formatted_balance&quot;: &quot;$1,450&quot;
      },
      {
        &quot;emplid&quot;: &quot;0001001&quot;,
        &quot;display_name&quot;: &quot;Nova Hart&quot;,
        &quot;term&quot;: &quot;2261&quot;,
        &quot;balance&quot;: 1050.0,
        &quot;formatted_balance&quot;: &quot;$1,050&quot;
      }
    ],
    &quot;balance_rule&quot;: &quot;BALANCE &gt; 0 means the student owes money. BALANCE &lt; 0 means the student has a credit.&quot;
  }
}</code></pre>
</div>
