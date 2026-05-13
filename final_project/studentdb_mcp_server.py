from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel


COURSE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = COURSE_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from studentdb_tools import (  # noqa: E402
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
    get_operator_access,
    get_student_balance,
    get_student_checklists,
    get_student_classes,
    get_student_financial_aid,
    get_student_holds,
    get_student_profile,
    get_student_requirements,
    list_database_objects,
    money,
)


TOOL_NAMES = [
    "inspect_schema",
    "inspect_row_security",
    "search_students",
    "list_active_students",
    "get_student_profile",
    "get_student_classes",
    "get_student_balance",
    "get_student_holds",
    "get_student_checklists",
    "get_student_requirements",
    "get_student_financial_aid",
    "find_students_with_holds",
    "find_students_with_positive_balances",
    "find_students_by_gpa",
    "find_students_with_incomplete_requirements",
    "find_students_with_checklist_items",
    "find_academic_risk_students",
    "create_student_success_report",
]


mcp = FastMCP(
    "StudentDB Assistant",
    instructions=(
        "Read-only MCP tools for the StudentDB Assistant course. Use these "
        "tools for facts from student_mock.db. Respect STUDENTDB_OPRID row "
        "security. Never invent student records."
    ),
)


def deps() -> DatabaseDeps:
    return DatabaseDeps()


def as_jsonable(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump()
    if isinstance(value, list):
        return [as_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: as_jsonable(item) for key, item in value.items()}
    return value


def resolve_student_ref(student_ref: str) -> dict[str, Any] | None:
    matches = find_students(deps(), student_ref)
    return matches[0] if matches else None


@mcp.tool()
def inspect_schema() -> dict[str, Any]:
    """List the real tables and views in student_mock.db."""
    return {"objects": list_database_objects(deps())}


@mcp.tool()
def inspect_row_security() -> dict[str, Any]:
    """Show the current STUDENTDB_OPRID profile and visible student rows."""
    return get_operator_access(deps())


@mcp.tool()
def search_students(student_ref: str) -> dict[str, Any]:
    """Search visible students by EMPLID or display name."""
    return {"students": find_students(deps(), student_ref)}


@mcp.tool()
def list_active_students() -> dict[str, Any]:
    """List visible students with PROG_STATUS = 'AC'."""
    rows = fetch_all(
        deps(),
        """
        SELECT s.EMPLID, s.DISPLAY_NAME, s.FERPA_FLAG, s.PROG_DESCR, s.PLAN_DESCR, s.CUM_GPA
        FROM V_STUDENT_360 s
        JOIN PS_SCRTY_STUDENT sec
          ON sec.EMPLID = s.EMPLID
         AND sec.OPRID = ?
        WHERE s.PROG_STATUS = 'AC'
        ORDER BY s.EMPLID
        """,
        (deps().oprid,),
    )
    return {"students": rows}


@mcp.tool(name="get_student_profile")
def get_student_profile_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's profile, program, plan, GPA, and FERPA flag."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    profile = get_student_profile(deps(), student["EMPLID"])
    return {"found": profile is not None, "profile": as_jsonable(profile)}


@mcp.tool(name="get_student_classes")
def get_student_classes_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's class enrollment rows."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    return {
        "found": True,
        "student": student,
        "classes": as_jsonable(get_student_classes(deps(), student["EMPLID"])),
    }


@mcp.tool(name="get_student_balance")
def get_student_balance_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's account balance. Positive means the student owes money."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    balance = get_student_balance(deps(), student["EMPLID"])
    return {
        "found": balance is not None,
        "student": student,
        "balance": as_jsonable(balance),
        "formatted_balance": money(balance.balance) if balance else None,
        "student_owes_money": bool(balance and balance.balance > 0),
        "student_has_credit": bool(balance and balance.balance < 0),
        "balance_rule": "BALANCE > 0 means the student owes money. BALANCE < 0 means the student has a credit.",
    }


@mcp.tool(name="get_student_holds")
def get_student_holds_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's holds/service indicators."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    return {
        "found": True,
        "student": student,
        "holds": as_jsonable(get_student_holds(deps(), student["EMPLID"])),
    }


@mcp.tool(name="get_student_checklists")
def get_student_checklists_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's checklist items."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    return {
        "found": True,
        "student": student,
        "checklists": as_jsonable(get_student_checklists(deps(), student["EMPLID"])),
    }


@mcp.tool(name="get_student_requirements")
def get_student_requirements_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's degree requirements and incomplete requirements."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    requirements = get_student_requirements(deps(), student["EMPLID"])
    incomplete = [row for row in requirements if row.status == "Not Satisfied"]
    return {
        "found": True,
        "student": student,
        "requirements": as_jsonable(requirements),
        "incomplete_requirements": as_jsonable(incomplete),
    }


@mcp.tool(name="get_student_financial_aid")
def get_student_financial_aid_tool(student_ref: str) -> dict[str, Any]:
    """Get a visible student's financial aid awards."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    awards = get_student_financial_aid(deps(), student["EMPLID"])
    return {"found": True, "student": student, "financial_aid": as_jsonable(awards)}


@mcp.tool(name="find_students_with_holds")
def find_students_with_holds_tool() -> dict[str, Any]:
    """List visible students with holds/service indicators."""
    return {"holds": as_jsonable(find_students_with_holds(deps()))}


@mcp.tool(name="find_students_with_positive_balances")
def find_students_with_positive_balances_tool() -> dict[str, Any]:
    """List visible students with BALANCE > 0."""
    balances = find_students_with_positive_balance(deps())
    return {
        "balances": [
            row.model_dump() | {"formatted_balance": money(row.balance)}
            for row in balances
        ],
        "balance_rule": "BALANCE > 0 means the student owes money. BALANCE < 0 means the student has a credit.",
    }


@mcp.tool(name="find_students_by_gpa")
def find_students_by_gpa_tool(max_gpa: float = 2.5) -> dict[str, Any]:
    """List visible students with CUM_GPA below max_gpa."""
    return {"max_gpa": max_gpa, "students": as_jsonable(find_students_by_gpa(deps(), max_gpa))}


@mcp.tool(name="find_students_with_incomplete_requirements")
def find_students_with_incomplete_requirements_tool() -> dict[str, Any]:
    """List visible students with Not Satisfied requirement rows."""
    return {"requirements": as_jsonable(find_students_with_incomplete_requirements(deps()))}


@mcp.tool(name="find_students_with_checklist_items")
def find_students_with_checklist_items_tool() -> dict[str, Any]:
    """List visible students with checklist items."""
    return {"checklists": as_jsonable(find_students_with_checklist_items(deps()))}


@mcp.tool(name="find_academic_risk_students")
def find_academic_risk_students_tool(max_gpa: float = 3.0) -> dict[str, Any]:
    """List visible academic-risk students using a GPA threshold."""
    return {"max_gpa": max_gpa, "students": as_jsonable(find_academic_risk_students(deps(), max_gpa))}


@mcp.tool(name="create_student_success_report")
def create_student_success_report_tool(student_ref: str) -> dict[str, Any]:
    """Create a structured advisor-ready report for a visible student."""
    student = resolve_student_ref(student_ref)
    if not student:
        return {"found": False, "message": "No visible matching student was found."}
    report = create_student_success_report(deps(), student["EMPLID"])
    return {"found": True, "student": student, "report": as_jsonable(report)}


def smoke_test() -> dict[str, Any]:
    return {
        "server": "StudentDB Assistant MCP",
        "oprid": deps().oprid,
        "tool_count": len(TOOL_NAMES),
        "tools": TOOL_NAMES,
        "row_security": inspect_row_security(),
        "zara_profile": get_student_profile_tool("Zara Quinn"),
        "positive_balances": find_students_with_positive_balances_tool(),
    }


def main() -> None:
    if "--list-tools" in sys.argv:
        print("\n".join(TOOL_NAMES))
        return
    if "--smoke-test" in sys.argv:
        print(json.dumps(smoke_test(), indent=2))
        return

    transport = os.getenv("STUDENTDB_MCP_TRANSPORT", "stdio")
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()
