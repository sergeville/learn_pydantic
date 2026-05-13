from __future__ import annotations

import os
import re
import sys
from typing import Any

from pydantic import BaseModel
from pydantic_ai import Agent


os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434/v1")

from .studentdb_tools import (
    DatabaseDeps,
    create_student_success_report,
    fetch_all,
    find_students,
    find_students_by_gpa,
    find_students_with_holds,
    find_students_with_positive_balance,
    get_student_balance,
    get_student_checklists,
    get_student_classes,
    get_student_requirements,
    money,
)


class RoutedAnswer(BaseModel):
    route: str
    question: str
    evidence: dict[str, Any]


def all_students(deps: DatabaseDeps) -> list[dict[str, Any]]:
    return fetch_all(
        deps,
        """
        SELECT p.EMPLID, p.DISPLAY_NAME, p.FERPA_FLAG
        FROM CS_CC_PERSON p
        JOIN PS_SCRTY_STUDENT sec
          ON sec.EMPLID = p.EMPLID
         AND sec.OPRID = ?
        ORDER BY p.EMPLID
        """,
        (deps.oprid,),
    )


def first_number(text: str, default: float | None = None) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else default


def resolve_student(deps: DatabaseDeps, question: str) -> dict[str, Any] | None:
    emplid_match = re.search(r"\b\d{7}\b", question)
    if emplid_match:
        matches = find_students(deps, emplid_match.group())
        return matches[0] if matches else None

    normalized = question.lower()
    for student in all_students(deps):
        if student["DISPLAY_NAME"].lower() in normalized:
            return student
    return None


def find_active_students(deps: DatabaseDeps) -> list[dict[str, Any]]:
    return fetch_all(
        deps,
        """
        SELECT s.EMPLID, s.DISPLAY_NAME, s.FERPA_FLAG, s.PROG_DESCR, s.PLAN_DESCR, s.CUM_GPA
        FROM V_STUDENT_360 s
        JOIN PS_SCRTY_STUDENT sec
          ON sec.EMPLID = s.EMPLID
         AND sec.OPRID = ?
        WHERE s.PROG_STATUS = 'AC'
        ORDER BY s.EMPLID
        """,
        (deps.oprid,),
    )


def route_question(deps: DatabaseDeps, question: str) -> RoutedAnswer:
    normalized = question.lower()

    if "hold" in normalized and any(word in normalized for word in ["which", "who", "list", "students"]):
        return RoutedAnswer(
            route="students_with_holds",
            question=question,
            evidence={"holds": [row.model_dump() for row in find_students_with_holds(deps)]},
        )

    if any(word in normalized for word in ["owe", "owes", "ows", "outstanding balance", "balance due"]):
        return RoutedAnswer(
            route="positive_balances",
            question=question,
            evidence={"balances": [row.model_dump() for row in find_students_with_positive_balance(deps)]},
        )

    if "active" in normalized and "program" in normalized:
        return RoutedAnswer(
            route="active_students",
            question=question,
            evidence={"students": find_active_students(deps)},
        )

    if "gpa" in normalized and ("below" in normalized or "under" in normalized):
        max_gpa = first_number(question, 2.5) or 2.5
        return RoutedAnswer(
            route="gpa_below",
            question=question,
            evidence={
                "max_gpa": max_gpa,
                "students": [row.model_dump() for row in find_students_by_gpa(deps, max_gpa)],
            },
        )

    student = resolve_student(deps, question)
    if not student:
        return RoutedAnswer(route="no_match", question=question, evidence={})

    emplid = student["EMPLID"]

    if "requirement" in normalized or "incomplete" in normalized:
        requirements = [
            row.model_dump()
            for row in get_student_requirements(deps, emplid)
            if row.status == "Not Satisfied"
        ]
        return RoutedAnswer(route="requirements", question=question, evidence={"requirements": requirements})

    if "checklist" in normalized or "due" in normalized:
        return RoutedAnswer(
            route="checklists",
            question=question,
            evidence={"checklists": [row.model_dump() for row in get_student_checklists(deps, emplid)]},
        )

    if "class" in normalized or "taking" in normalized:
        return RoutedAnswer(
            route="classes",
            question=question,
            evidence={"classes": [row.model_dump() for row in get_student_classes(deps, emplid)]},
        )

    if "balance" in normalized:
        balance = get_student_balance(deps, emplid)
        return RoutedAnswer(
            route="balance",
            question=question,
            evidence={"balance": balance.model_dump() if balance else None},
        )

    report = create_student_success_report(deps, emplid)
    return RoutedAnswer(route="student_report", question=question, evidence={"report": report.model_dump()})


def format_answer(answer: RoutedAnswer) -> str:
    if answer.route == "students_with_holds":
        lines = ["Students with holds:"]
        for row in answer.evidence["holds"]:
            lines.append(f"- {row['display_name']} ({row['emplid']}): {row['code']}, {row['reason']}, impact {row['impact']}")
        return "\n".join(lines)

    if answer.route == "positive_balances":
        lines = ["Students with positive balances:"]
        for row in answer.evidence["balances"]:
            lines.append(f"- {row['display_name']} ({row['emplid']}): term {row['term']}, balance {money(row['balance'])}")
        if not answer.evidence["balances"]:
            lines.append("- No visible students have positive balances.")
        return "\n".join(lines)

    if answer.route == "active_students":
        lines = ["Students active in their academic program:"]
        for row in answer.evidence["students"]:
            privacy = " FERPA_FLAG=Y" if row["FERPA_FLAG"] == "Y" else ""
            lines.append(f"- {row['DISPLAY_NAME']} ({row['EMPLID']}): {row['PROG_DESCR']} / {row['PLAN_DESCR']}{privacy}")
        return "\n".join(lines)

    if answer.route == "gpa_below":
        lines = [f"Students with GPA below {answer.evidence['max_gpa']}:"]
        for row in answer.evidence["students"]:
            privacy = " FERPA_FLAG=Y" if row["ferpa_flag"] == "Y" else ""
            lines.append(f"- {row['display_name']} ({row['emplid']}): GPA {row['gpa']}{privacy}")
        if not answer.evidence["students"]:
            lines.append("- No students found.")
        return "\n".join(lines)

    if answer.route == "requirements":
        lines = ["Incomplete requirements:"]
        for row in answer.evidence["requirements"]:
            lines.append(f"- {row['requirement_group']}: {row['requirement']} ({row['units_completed']}/{row['units_required']} units)")
        if not answer.evidence["requirements"]:
            lines.append("- No incomplete requirements listed.")
        return "\n".join(lines)

    if answer.route == "checklists":
        lines = ["Checklist items:"]
        for row in answer.evidence["checklists"]:
            lines.append(f"- {row['item']}: {row['description']} ({row['status']}, due {row['due_date'] or 'not listed'})")
        if not answer.evidence["checklists"]:
            lines.append("- No checklist items listed.")
        return "\n".join(lines)

    if answer.route == "classes":
        lines = ["Classes:"]
        for row in answer.evidence["classes"]:
            grade = row["grade"] or "not listed"
            lines.append(f"- {row['subject']} {row['catalog_number']}: {row['course']} ({row['enrollment_status']}, {row['units']} units, grade {grade})")
        if not answer.evidence["classes"]:
            lines.append("- No classes listed.")
        return "\n".join(lines)

    if answer.route == "balance":
        balance = answer.evidence["balance"]
        if not balance:
            return "No balance listed."
        return f"Balance for {balance['display_name']} ({balance['emplid']}): term {balance['term']}, {money(balance['balance'])}"

    if answer.route == "student_report":
        report = answer.evidence["report"]
        profile = report["profile"]
        balance = report["balance"]
        lines = [
            f"Student success report for {profile['display_name']} ({profile['emplid']})",
            f"- FERPA flag: {profile['ferpa_flag']}",
            f"- Program: {profile['program']} ({profile['program_status']})",
            f"- Plan: {profile['plan']}",
            f"- GPA: {profile['gpa']}",
            f"- Balance: {money(balance['balance']) if balance else 'not listed'}",
            "",
            "Holds:",
        ]
        for row in report["holds"]:
            lines.append(f"- {row['code']}: {row['reason']} (impact {row['impact']})")
        if not report["holds"]:
            lines.append("- No holds listed.")
        lines.append("")
        lines.append("Incomplete requirements:")
        for row in report["incomplete_requirements"]:
            lines.append(f"- {row['requirement_group']}: {row['requirement']}")
        if not report["incomplete_requirements"]:
            lines.append("- No incomplete requirements listed.")
        return "\n".join(lines)

    return f"No matching student was found for: {answer.question}"


def ai_summary(answer: RoutedAnswer) -> str:
    summary_agent = Agent(
        os.getenv("PYDANTIC_AI_MODEL", "ollama:llama3.2"),
        output_type=str,
        model_settings={"temperature": 0},
        system_prompt=(
            "Summarize only the JSON evidence. Do not invent records. Preserve "
            "balance signs and mention FERPA_FLAG=Y if present."
        ),
    )
    return summary_agent.run_sync(
        "Summarize this StudentDB Assistant answer evidence:\n"
        f"{answer.model_dump_json(indent=2)}"
    ).output


def main() -> None:
    deps = DatabaseDeps()
    question = "Show me Zara Quinn" if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    routed = route_question(deps, question)
    print(format_answer(routed))
    if os.getenv("USE_AI_SUMMARY") == "1":
        print("\nAI summary:")
        print(ai_summary(routed))


if __name__ == "__main__":
    main()
