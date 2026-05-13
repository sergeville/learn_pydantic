from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.exceptions import UnexpectedModelBehavior


os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434/v1")

from .studentdb_tools import (
    DatabaseDeps,
    create_student_success_report,
    fetch_all,
    find_academic_risk_students,
    find_students,
    find_students_by_gpa,
    find_students_with_checklist_items,
    find_students_with_holds,
    find_students_with_incomplete_requirements,
    find_students_with_positive_balance,
    get_student_balance,
    get_student_checklists,
    get_student_classes,
    get_student_financial_aid,
    get_student_holds,
    get_student_profile,
    get_student_requirements,
    get_operator_access,
    list_database_objects,
    money,
)


@dataclass
class ConversationDeps:
    database: DatabaseDeps
    current_emplid: str | None = None
    current_student_name: str | None = None


class ChatAnswer(BaseModel):
    answer: str = Field(description="Plain-English answer for the user.")
    used_tools: list[str] = Field(default_factory=list)
    privacy_notes: list[str] = Field(default_factory=list)


def safe_rows(rows: list[BaseModel] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        if isinstance(row, BaseModel):
            output.append(row.model_dump())
        else:
            output.append(row)
    return output


def references_current_student(text: str | None) -> bool:
    if not text:
        return True
    normalized = text.lower()
    return any(
        phrase in normalized
        for phrase in [
            "this student",
            "current student",
            "selected student",
            "that student",
            "them",
            "their",
        ]
    )


def find_student_in_text(deps: ConversationDeps, text: str | None) -> dict[str, Any] | None:
    if text:
        emplid_match = re.search(r"\b\d{7}\b", text)
        if emplid_match:
            matches = find_students(deps.database, emplid_match.group())
            if matches:
                return matches[0]

        normalized = text.lower()
        for student in fetch_all(
            deps.database,
            """
            SELECT p.EMPLID, p.DISPLAY_NAME, p.FERPA_FLAG
            FROM CS_CC_PERSON p
            JOIN PS_SCRTY_STUDENT sec
              ON sec.EMPLID = p.EMPLID
             AND sec.OPRID = ?
            ORDER BY p.EMPLID
            """,
            (deps.database.oprid,),
        ):
            if student["DISPLAY_NAME"].lower() in normalized:
                return student

        matches = find_students(deps.database, text)
        if matches:
            return matches[0]

    if references_current_student(text) and deps.current_emplid:
        matches = find_students(deps.database, deps.current_emplid)
        if matches:
            return matches[0]

    return None


def set_current_student(deps: ConversationDeps, student: dict[str, Any]) -> None:
    deps.current_emplid = student["EMPLID"]
    deps.current_student_name = student["DISPLAY_NAME"]


studentdb_agent = Agent(
    os.getenv("PYDANTIC_AI_MODEL", "ollama:llama3.2"),
    deps_type=ConversationDeps,
    output_type=ChatAnswer,
    tool_retries=1,
    output_retries=1,
    model_settings={"temperature": 0},
    system_prompt=(
        "You are StudentDB Assistant, a read-only student information chatbot. "
        "You must use tools for database facts. The user does not know SQL. "
        "Use the current selected student when the user says 'this student'. "
        "Do not invent student data. If a tool returns no rows, say the answer "
        "could not be found in the database. Preserve balance signs exactly: "
        "positive balance means the student owes money; negative balance means "
        "a credit/institution owes the student. If FERPA_FLAG is Y, mention "
        "that the record may have privacy restrictions. Return concise answers."
    ),
)


@studentdb_agent.tool
async def inspect_schema(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """List the actual tables and views available in student_mock.db."""
    return {"objects": list_database_objects(ctx.deps.database)}


@studentdb_agent.tool
async def inspect_row_security(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """Show the current mock OPRID row-security profile and allowed students."""
    return get_operator_access(ctx.deps.database)


@studentdb_agent.tool
async def select_student(ctx: RunContext[ConversationDeps], student_ref: str) -> dict[str, Any]:
    """Find a student by EMPLID or name and make that student the current conversation subject."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    return {"found": True, "student": student}


@studentdb_agent.tool
async def get_current_student(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """Return the current selected student for follow-up questions."""
    student = find_student_in_text(ctx.deps, None)
    if not student:
        return {"found": False, "message": "No student is selected yet."}
    return {"found": True, "student": student}


@studentdb_agent.tool
async def get_student_profile_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get profile/program/plan/GPA details from V_STUDENT_360."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    profile = get_student_profile(ctx.deps.database, student["EMPLID"])
    return {"found": profile is not None, "profile": profile.model_dump() if profile else None}


@studentdb_agent.tool
async def get_student_classes_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get class enrollment rows from V_STUDENT_CLASSES."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    return {"student": student, "classes": safe_rows(get_student_classes(ctx.deps.database, student["EMPLID"]))}


@studentdb_agent.tool
async def get_student_balance_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get account balance from V_STUDENT_BALANCE."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    balance = get_student_balance(ctx.deps.database, student["EMPLID"])
    return {
        "student": student,
        "balance": balance.model_dump() if balance else None,
        "formatted_balance": money(balance.balance) if balance else None,
        "student_owes_money": bool(balance and balance.balance > 0),
        "student_has_credit": bool(balance and balance.balance < 0),
    }


@studentdb_agent.tool
async def get_student_holds_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get holds/service indicators from V_STUDENT_HOLDS."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    return {"student": student, "holds": safe_rows(get_student_holds(ctx.deps.database, student["EMPLID"]))}


@studentdb_agent.tool
async def get_student_checklists_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get checklist items from V_STUDENT_CHECKLISTS."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    return {"student": student, "checklists": safe_rows(get_student_checklists(ctx.deps.database, student["EMPLID"]))}


@studentdb_agent.tool
async def get_student_requirements_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get degree requirements from V_STUDENT_REQUIREMENTS."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    requirements = get_student_requirements(ctx.deps.database, student["EMPLID"])
    incomplete = [row for row in requirements if row.status == "Not Satisfied"]
    return {
        "student": student,
        "requirements": safe_rows(requirements),
        "incomplete_requirements": safe_rows(incomplete),
    }


@studentdb_agent.tool
async def get_student_financial_aid_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Get financial aid awards from CS_FA_AWARD."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    awards = get_student_financial_aid(ctx.deps.database, student["EMPLID"])
    return {"student": student, "financial_aid": safe_rows(awards)}


@studentdb_agent.tool
async def create_student_success_report_tool(ctx: RunContext[ConversationDeps], student_ref: str | None = None) -> dict[str, Any]:
    """Create a structured advisor-ready student success report."""
    student = find_student_in_text(ctx.deps, student_ref)
    if not student:
        return {"found": False, "message": "No matching student found."}
    set_current_student(ctx.deps, student)
    report = create_student_success_report(ctx.deps.database, student["EMPLID"])
    return {"student": student, "report": report.model_dump()}


@studentdb_agent.tool
async def find_students_with_holds_tool(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """List all students with holds/service indicators."""
    return {"holds": safe_rows(find_students_with_holds(ctx.deps.database))}


@studentdb_agent.tool
async def find_students_with_positive_balances_tool(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """List students with BALANCE > 0, meaning the student owes money."""
    balances = find_students_with_positive_balance(ctx.deps.database)
    return {
        "balances": [row.model_dump() | {"formatted_balance": money(row.balance)} for row in balances],
        "balance_rule": "BALANCE > 0 means student owes money. BALANCE < 0 means student has a credit.",
    }


@studentdb_agent.tool
async def find_students_by_gpa_tool(ctx: RunContext[ConversationDeps], max_gpa: float) -> dict[str, Any]:
    """List students with CUM_GPA below max_gpa from V_STUDENT_360."""
    return {"max_gpa": max_gpa, "students": safe_rows(find_students_by_gpa(ctx.deps.database, max_gpa))}


@studentdb_agent.tool
async def find_students_with_incomplete_requirements_tool(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """List all students with Not Satisfied requirement rows."""
    return {"requirements": safe_rows(find_students_with_incomplete_requirements(ctx.deps.database))}


@studentdb_agent.tool
async def find_students_with_checklist_items_tool(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """List all students with checklist items."""
    return {"checklists": safe_rows(find_students_with_checklist_items(ctx.deps.database))}


@studentdb_agent.tool
async def find_academic_risk_students_tool(ctx: RunContext[ConversationDeps], max_gpa: float = 3.0) -> dict[str, Any]:
    """List students at academic risk using a GPA threshold. Default threshold is below 3.0 in this mock dataset."""
    return {"max_gpa": max_gpa, "students": safe_rows(find_academic_risk_students(ctx.deps.database, max_gpa))}


@studentdb_agent.tool
async def find_active_students_tool(ctx: RunContext[ConversationDeps]) -> dict[str, Any]:
    """List students active in their academic program using PROG_STATUS = 'AC'."""
    rows = fetch_all(
        ctx.deps.database,
        """
        SELECT s.EMPLID, s.DISPLAY_NAME, s.FERPA_FLAG, s.PROG_DESCR, s.PLAN_DESCR, s.CUM_GPA
        FROM V_STUDENT_360 s
        JOIN PS_SCRTY_STUDENT sec
          ON sec.EMPLID = s.EMPLID
         AND sec.OPRID = ?
        WHERE s.PROG_STATUS = 'AC'
        ORDER BY s.EMPLID
        """,
        (ctx.deps.database.oprid,),
    )
    return {"students": rows}


def deterministic_tool_fallback(deps: ConversationDeps, user_text: str) -> ChatAnswer:
    """Keep the terminal chatbot useful when a local model cannot call tools."""
    normalized = user_text.lower()
    privacy_notes: list[str] = []

    asks_about_owing = any(word in normalized for word in ["owe", "owes", "ows", "outstanding balance", "balance due"])
    asks_for_global_list = any(word in normalized for word in ["which", "who", "list", "all students"])

    if "hold" in normalized and any(word in normalized for word in ["which", "who", "list", "students"]):
        holds = find_students_with_holds(deps.database)
        answer = "\n".join(f"- {h.display_name} ({h.emplid}): {h.code}, {h.reason}" for h in holds)
        return ChatAnswer(answer=f"Students with holds:\n{answer}", used_tools=["find_students_with_holds_tool"], privacy_notes=[])

    if asks_about_owing and not asks_for_global_list:
        student = find_student_in_text(deps, user_text)
        if student:
            set_current_student(deps, student)
            profile = get_student_profile(deps.database, student["EMPLID"])
            balance = get_student_balance(deps.database, student["EMPLID"])
            if profile and profile.ferpa_flag == "Y":
                privacy_notes.append("FERPA_FLAG is Y; this record may have privacy restrictions.")
            if not balance:
                return ChatAnswer(
                    answer=f"No balance row was found for {student['DISPLAY_NAME']}.",
                    used_tools=["get_student_balance_tool"],
                    privacy_notes=privacy_notes,
                )
            if balance.balance > 0:
                answer = f"Yes. {student['DISPLAY_NAME']} has a positive balance of {money(balance.balance)}."
            elif balance.balance < 0:
                answer = f"No. {student['DISPLAY_NAME']} has a credit balance of {money(balance.balance)}."
            else:
                answer = f"No. {student['DISPLAY_NAME']} has a zero balance."
            return ChatAnswer(answer=answer, used_tools=["get_student_balance_tool"], privacy_notes=privacy_notes)

    if asks_about_owing:
        balances = find_students_with_positive_balance(deps.database)
        answer = "\n".join(f"- {b.display_name} ({b.emplid}): {money(b.balance)}" for b in balances)
        if not answer:
            answer = "- No visible students have positive balances."
        return ChatAnswer(answer=f"Students with positive balances:\n{answer}", used_tools=["find_students_with_positive_balances_tool"], privacy_notes=[])

    student = find_student_in_text(deps, user_text)
    if student:
        set_current_student(deps, student)
        profile = get_student_profile(deps.database, student["EMPLID"])
        if profile and profile.ferpa_flag == "Y":
            privacy_notes.append("FERPA_FLAG is Y; this record may have privacy restrictions.")
        if "class" in normalized or "taking" in normalized:
            classes = get_student_classes(deps.database, student["EMPLID"])
            lines = [f"{student['DISPLAY_NAME']} is enrolled in:"]
            lines.extend(f"- {c.subject} {c.catalog_number}: {c.course}" for c in classes)
            return ChatAnswer(answer="\n".join(lines), used_tools=["get_student_classes_tool"], privacy_notes=privacy_notes)
        if "hold" in normalized:
            holds = get_student_holds(deps.database, student["EMPLID"])
            if not holds:
                return ChatAnswer(answer=f"{student['DISPLAY_NAME']} has no holds listed.", used_tools=["get_student_holds_tool"], privacy_notes=privacy_notes)
            lines = [f"{student['DISPLAY_NAME']} has these holds:"]
            lines.extend(f"- {h.code}: {h.reason} (impact {h.impact})" for h in holds)
            return ChatAnswer(answer="\n".join(lines), used_tools=["get_student_holds_tool"], privacy_notes=privacy_notes)
        if "financial aid" in normalized or "aid" in normalized:
            awards = get_student_financial_aid(deps.database, student["EMPLID"])
            if not awards:
                return ChatAnswer(answer=f"No financial aid awards were found for {student['DISPLAY_NAME']}.", used_tools=["get_student_financial_aid_tool"], privacy_notes=privacy_notes)
            lines = [f"Financial aid for {student['DISPLAY_NAME']}:"]
            lines.extend(f"- {a.award}: offered {money(a.offer_amount)}, accepted {money(a.accept_amount)}, status {a.award_status}, disbursement {a.disbursement_status}" for a in awards)
            return ChatAnswer(answer="\n".join(lines), used_tools=["get_student_financial_aid_tool"], privacy_notes=privacy_notes)

        report = create_student_success_report(deps.database, student["EMPLID"])
        balance_text = money(report.balance.balance) if report.balance else "not listed"
        answer = (
            f"Advisor summary for {student['DISPLAY_NAME']} ({student['EMPLID']}):\n"
            f"- Program: {profile.program if profile else 'not listed'}\n"
            f"- GPA: {profile.gpa if profile else 'not listed'}\n"
            f"- Balance: {balance_text}\n"
            f"- Holds: {len(report.holds)}\n"
            f"- Incomplete requirements: {len(report.incomplete_requirements)}"
        )
        return ChatAnswer(answer=answer, used_tools=["create_student_success_report_tool"], privacy_notes=privacy_notes)

    return ChatAnswer(
        answer="I could not find that answer in the database. Try naming a student or asking about holds, balances, GPA, checklist items, or active students.",
        used_tools=[],
        privacy_notes=[],
    )


def print_chat_answer(answer: ChatAnswer) -> None:
    print(f"\nAgent: {answer.answer}")
    if answer.privacy_notes:
        for note in answer.privacy_notes:
            print(f"Privacy note: {note}")
    if answer.used_tools:
        print(f"Tools used: {', '.join(answer.used_tools)}")


def chat_loop() -> None:
    deps = ConversationDeps(database=DatabaseDeps())
    message_history: list[Any] = []
    mode = os.getenv("STUDENTDB_AGENT_MODE", "safe").lower()

    print("StudentDB Conversational Agent")
    print("Type a question, or type exit to quit.")
    print("Example: Tell me about student 0001005")
    print(f"Mode: {mode}")
    if mode != "tools":
        print("Set STUDENTDB_AGENT_MODE=tools to try Pydantic AI tool-calling with a tool-capable model.")

    while True:
        user_text = input("\nUser: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            print("Agent: Goodbye.")
            break
        if not user_text:
            continue

        if mode != "tools":
            fallback = deterministic_tool_fallback(deps, user_text)
            print_chat_answer(fallback)
            continue

        try:
            result = studentdb_agent.run_sync(user_text, deps=deps, message_history=message_history)
            message_history = result.all_messages()
            print_chat_answer(result.output)
        except (UnexpectedModelBehavior, Exception) as exc:
            fallback = deterministic_tool_fallback(deps, user_text)
            fallback.answer = (
                fallback.answer
                + "\n\nNote: The model could not complete a Pydantic AI tool call, "
                + "so the safe deterministic database fallback answered this turn."
            )
            print_chat_answer(fallback)
            if os.getenv("STUDENTDB_DEBUG") == "1":
                print(f"Debug error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    chat_loop()
