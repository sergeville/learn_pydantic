# Syllabus: StudentDB Assistant

## Course Goal

Build a Pydantic AI assistant that answers student-information questions using
the real SQLite database in `data/student_mock.db`.

## Learning Outcomes

By the end, a learner can:

- Connect Python to SQLite.
- Inspect real tables and views.
- Query student profile, class, balance, hold, checklist, and requirement data.
- Convert database rows into Pydantic models.
- Build safe read-only query tools.
- Use Pydantic AI for evidence-based summaries.
- Expose the same database tools through MCP for compatible AI clients.
- Avoid common AI/database safety mistakes.
- Build a complete command-line StudentDB Assistant.

## Modules

1. SQLite connection and schema inspection
2. Pydantic models for student records
3. Read-only database tools
4. Pydantic AI summaries from trusted evidence
5. Command-line routing for student questions
6. Final project: StudentDB Assistant
7. Conversational terminal agent with Pydantic AI tools
8. PeopleSoft-inspired row security with mock `OPRID` access
9. Optional MCP server for reusing StudentDB tools in MCP clients

## Database Objects Used

Tables:

- `CS_CC_PERSON`
- `CS_SR_ACAD_PROGRAM`
- `CS_SR_ACAD_PLAN`
- `CS_SR_TERM_ENROLLMENT`
- `CS_SR_CLASS_ENROLLMENT`
- `CS_SR_CLASS_SCHEDULE`
- `CS_SR_COURSE_CATALOG`
- `CS_FA_AWARD`
- `CS_SF_ACCOUNT_ITEM`
- `CS_CC_CHECKLIST`
- `CS_CC_SERVICE_INDICATOR`
- `CS_AA_REQUIREMENT_STATUS`

Views:

- `V_STUDENT_360`
- `V_STUDENT_CLASSES`
- `V_STUDENT_BALANCE`
- `V_STUDENT_CHECKLISTS`
- `V_STUDENT_HOLDS`
- `V_STUDENT_REQUIREMENTS`

## Assessment

- Run every script successfully.
- Complete the practice exercises.
- Extend the final project with one new route.
- Explain why exact database values are formatted by Python instead of the AI
  model.
- Demonstrate that `STUDENTDB_OPRID=ADVISOR_COMP` can see Computer Science
  students but cannot see Business Analytics students.
- Run the MCP smoke test and explain why MCP wraps existing tools instead of
  creating a second SQL/query layer.

## Row Security Requirement

All student-facing query tools must respect the current `STUDENTDB_OPRID`.
The training security model uses:

- `PS_SCRTY_OPR`
- `PS_SCRTY_STUDENT`
- `V_ROW_SECURITY_ACCESS`

This is PeopleSoft-inspired for teaching. It is not a replacement for real
PeopleSoft security administration.

## MCP Extension

Lesson 9 shows how to expose the same read-only, row-security-aware database
tools through an MCP server. MCP is an integration layer for other AI clients;
it does not replace Pydantic AI or the command-line chatbot.
