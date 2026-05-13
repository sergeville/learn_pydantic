from __future__ import annotations

import re
import sys

from studentdb_tools import (
    DatabaseDeps,
    create_student_success_report,
    find_students,
    find_students_with_holds,
    find_students_with_positive_balance,
    get_student_classes,
    money,
)


def find_student_from_question(deps: DatabaseDeps, question: str) -> dict | None:
    emplid_match = re.search(r"\b\d{7}\b", question)
    if emplid_match:
        matches = find_students(deps, emplid_match.group())
        return matches[0] if matches else None

    for word_count in [2, 1]:
        words = question.split()
        for index in range(len(words) - word_count + 1):
            phrase = " ".join(words[index : index + word_count]).strip("?.!,")
            matches = find_students(deps, phrase)
            if matches:
                return matches[0]
    return None


def answer_question(question: str) -> str:
    deps = DatabaseDeps()
    normalized = question.lower()

    if "hold" in normalized:
        lines = ["Students with holds:"]
        for hold in find_students_with_holds(deps):
            lines.append(f"- {hold.display_name} ({hold.emplid}): {hold.code}, {hold.reason}")
        return "\n".join(lines)

    if any(word in normalized for word in ["owe", "owes", "ows", "balance due"]):
        lines = ["Students with positive balances:"]
        for balance in find_students_with_positive_balance(deps):
            lines.append(f"- {balance.display_name} ({balance.emplid}): {money(balance.balance)}")
        return "\n".join(lines)

    student = find_student_from_question(deps, question)
    if not student:
        return "No matching route or student found."

    if "class" in normalized or "taking" in normalized:
        lines = [f"Classes for {student['DISPLAY_NAME']}:"]
        for row in get_student_classes(deps, student["EMPLID"]):
            grade = row.grade or "not listed"
            lines.append(f"- {row.subject} {row.catalog_number}: {row.course}, grade {grade}")
        return "\n".join(lines)

    report = create_student_success_report(deps, student["EMPLID"])
    profile = report.profile
    if not profile:
        return "No matching student found."
    balance = money(report.balance.balance) if report.balance else "not listed"
    return (
        f"{profile.display_name} ({profile.emplid})\n"
        f"- Program: {profile.program}\n"
        f"- Plan: {profile.plan}\n"
        f"- GPA: {profile.gpa}\n"
        f"- FERPA flag: {profile.ferpa_flag}\n"
        f"- Balance: {balance}\n"
        f"- Holds: {len(report.holds)}"
    )


if __name__ == "__main__":
    question = "Show me Zara Quinn" if len(sys.argv) == 1 else " ".join(sys.argv[1:])
    print(answer_question(question))
