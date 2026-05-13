from __future__ import annotations

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "test_outputs"
OUTPUT_FILE = OUTPUT_DIR / "student_self_service_stdout.txt"
REAL_DOWNLOADS_ROOT = str(Path.home() / "Downloads")
DISPLAY_DEV_ROOT = "~/Dev"


def display_paths(text: str) -> str:
    return text.replace(REAL_DOWNLOADS_ROOT, DISPLAY_DEV_ROOT)


def run_and_capture(command: list[str], env: dict[str, str] | None = None) -> str:
    process_env = os.environ.copy()
    if env:
        process_env.update(env)

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=process_env,
    )

    command_text = display_paths(" ".join(command))
    section = [
        f"$ {command_text}",
        f"exit_code={result.returncode}",
        "--- stdout ---",
        display_paths(result.stdout.rstrip()),
    ]
    if result.stderr:
        section.extend(["--- stderr ---", display_paths(result.stderr.rstrip())])
    section.append("")
    return "\n".join(section)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    env = {"STUDENTDB_OPRID": "STUDENT_0001005"}

    sections = [
        "Student self-service row-security stdout capture",
        f"created_at={datetime.now().isoformat(timespec='seconds')}",
        "operator=STUDENT_0001005",
        "expected_access=Zara Quinn only",
        "",
    ]

    commands = [
        [sys.executable, "final_project/studentdb_assistant.py", "Show me Zara Quinn"],
        [sys.executable, "final_project/studentdb_assistant.py", "Show me Theo Lane"],
        [sys.executable, "final_project/studentdb_assistant.py", "Which students owe money?"],
        [sys.executable, "final_project/studentdb_assistant.py", "What classes is Zara Quinn taking?"],
        [sys.executable, "final_project/conversational_studentdb_agent.py"],
    ]

    for command in commands[:-1]:
        sections.append(run_and_capture(command, env=env))

    chat_input = (
        "Tell me about student 0001005\n"
        "What classes is this student taking?\n"
        "Show me Theo Lane\n"
        "exit\n"
    )
    process_env = os.environ.copy()
    process_env.update(env)
    chat = subprocess.run(
        commands[-1],
        cwd=ROOT,
        text=True,
        input=chat_input,
        capture_output=True,
        env=process_env,
    )
    sections.extend(
        [
            "$ "
            + display_paths(" ".join(commands[-1]))
            + " <<'CHAT_INPUT'\n"
            + chat_input.rstrip()
            + "\nCHAT_INPUT",
            f"exit_code={chat.returncode}",
            "--- stdout ---",
            display_paths(chat.stdout.rstrip()),
        ]
    )
    if chat.stderr:
        sections.extend(["--- stderr ---", display_paths(chat.stderr.rstrip())])

    OUTPUT_FILE.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote transcript to {display_paths(str(OUTPUT_FILE))}")


if __name__ == "__main__":
    main()
