from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "student_mock.db"


def run(command: list[str], env: dict[str, str] | None = None) -> str:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        env=process_env,
    )
    return result.stdout


def assert_database() -> None:
    connection = sqlite3.connect(DB_PATH)
    try:
        person_count = connection.execute("SELECT count(*) FROM CS_CC_PERSON").fetchone()[0]
        view_count = connection.execute(
            "SELECT count(*) FROM sqlite_master WHERE type = 'view'"
        ).fetchone()[0]
        security_count = connection.execute(
            "SELECT count(*) FROM PS_SCRTY_STUDENT WHERE OPRID = 'ADVISOR_COMP'"
        ).fetchone()[0]
        student_self_service_count = connection.execute(
            "SELECT count(*) FROM PS_SCRTY_STUDENT WHERE OPRID LIKE 'STUDENT_%'"
        ).fetchone()[0]
    finally:
        connection.close()

    assert person_count == 15, f"Expected 15 people, found {person_count}"
    assert view_count >= 6, f"Expected at least 6 views, found {view_count}"
    assert security_count == 5, f"Expected 5 COMP-secured students, found {security_count}"
    assert student_self_service_count == 15, (
        f"Expected 15 student self-service rows, found {student_self_service_count}"
    )


def assert_scripts() -> None:
    run([sys.executable, "scripts/01_connect_sqlite.py"])

    holds = run([sys.executable, "final_project/studentdb_assistant.py", "Which students have holds?"])
    assert "Theo Lane" in holds
    assert "Orion Reed" in holds

    balances = run([sys.executable, "final_project/studentdb_assistant.py", "Which students owe money?"])
    assert "$2,650" in balances
    assert "-$250" not in balances

    requirements = run(
        [
            sys.executable,
            "final_project/studentdb_assistant.py",
            "Which requirements are incomplete for 0001012?",
        ]
    )
    assert "BSCS-CAPSTONE" in requirements

    chat = subprocess.run(
        [sys.executable, "final_project/conversational_studentdb_agent.py"],
        cwd=ROOT,
        check=True,
        text=True,
        input=(
            "Tell me about student 0001005\n"
            "What classes is this student taking?\n"
            "Does this student owe money?\n"
            "exit\n"
        ),
        capture_output=True,
    ).stdout
    assert "Zara Quinn" in chat
    assert "CS 101" in chat
    assert "credit balance of -$250" in chat

    advisor_comp_zara = run(
        [sys.executable, "final_project/studentdb_assistant.py", "Show me Zara Quinn"],
        env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
    )
    assert "Zara Quinn" in advisor_comp_zara

    advisor_comp_theo = run(
        [sys.executable, "final_project/studentdb_assistant.py", "Show me Theo Lane"],
        env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
    )
    assert "No matching student" in advisor_comp_theo

    advisor_comp_balances = run(
        [sys.executable, "final_project/studentdb_assistant.py", "Which students owe money?"],
        env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
    )
    assert "Orion Reed" in advisor_comp_balances
    assert "Theo Lane" not in advisor_comp_balances

    student_zara = run(
        [sys.executable, "final_project/studentdb_assistant.py", "Show me Zara Quinn"],
        env={"STUDENTDB_OPRID": "STUDENT_0001005"},
    )
    assert "Zara Quinn" in student_zara

    student_theo = run(
        [sys.executable, "final_project/studentdb_assistant.py", "Show me Theo Lane"],
        env={"STUDENTDB_OPRID": "STUDENT_0001005"},
    )
    assert "No matching student" in student_theo

    mcp_tools = run([sys.executable, "final_project/studentdb_mcp_server.py", "--list-tools"])
    assert "get_student_profile" in mcp_tools
    assert "create_student_success_report" in mcp_tools

    mcp_smoke = json.loads(run([sys.executable, "final_project/studentdb_mcp_server.py", "--smoke-test"]))
    assert mcp_smoke["tool_count"] == 18
    assert mcp_smoke["zara_profile"]["profile"]["display_name"] == "Zara Quinn"
    assert mcp_smoke["positive_balances"]["balance_rule"].startswith("BALANCE > 0")

    advisor_mcp_smoke = json.loads(
        run(
            [sys.executable, "final_project/studentdb_mcp_server.py", "--smoke-test"],
            env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
        )
    )
    assert advisor_mcp_smoke["row_security"]["allowed_count"] == 5
    advisor_names = {
        row["DISPLAY_NAME"]
        for row in advisor_mcp_smoke["row_security"]["allowed_students"]
    }
    assert "Zara Quinn" in advisor_names
    assert "Theo Lane" not in advisor_names

    packaged_cli = run(
        [sys.executable, "-m", "studentdb_assistant_course.cli", "Show me Zara Quinn"],
        env={"PYTHONPATH": "src"},
    )
    assert "Student success report for Zara Quinn" in packaged_cli

    packaged_mcp_tools = run(
        [sys.executable, "-m", "studentdb_assistant_course.mcp_server", "--list-tools"],
        env={"PYTHONPATH": "src"},
    )
    assert "get_student_balance" in packaged_mcp_tools


if __name__ == "__main__":
    assert_database()
    assert_scripts()
    print("Course validation passed.")
