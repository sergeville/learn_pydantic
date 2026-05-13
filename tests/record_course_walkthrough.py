from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "course_runs"
OUTPUT_FILE = OUTPUT_DIR / "student_course_walkthrough.md"
IMAGE_DIR = OUTPUT_DIR / "images"
REAL_DOWNLOADS_ROOT = str(Path.home() / "Downloads")
DISPLAY_DEV_ROOT = "~/Dev"


@dataclass
class Action:
    title: str
    description: str
    command: list[str] | None = None
    stdin: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    note: str | None = None


def shell_quote(parts: list[str]) -> str:
    quoted: list[str] = []
    for part in parts:
        if any(char.isspace() for char in part) or any(char in part for char in ['"', "'", "$"]):
            quoted.append(repr(part))
        else:
            quoted.append(part)
    return " ".join(quoted)


def display_paths(text: str) -> str:
    return text.replace(REAL_DOWNLOADS_ROOT, DISPLAY_DEV_ROOT)


def html_terminal_block(
    label: str,
    content: str,
    *,
    accent: str,
    header_bg: str,
    body_bg: str,
    text_color: str,
) -> str:
    safe_content = escape(display_paths(content.rstrip() or "(empty)"))
    safe_label = escape(label)
    return "\n".join(
        [
            f'<div style="border-left: 4px solid {accent}; background: {header_bg}; padding: 0.75rem 1rem; margin: 1rem 0; border-radius: 6px;">',
            f'  <div style="font-weight: 700; color: {accent}; margin-bottom: 0.5rem;">{safe_label}</div>',
            f'  <pre style="background: {body_bg}; color: {text_color}; padding: 0.85rem; margin: 0; overflow-x: auto; border-radius: 4px;"><code>{safe_content}</code></pre>',
            "</div>",
        ]
    )


def run_action(action: Action) -> str:
    lines = [f"## {action.title}", "", action.description, ""]

    if action.note:
        lines.extend([f"Note: {action.note}", ""])

    if not action.command:
        lines.extend(["No command was run for this action.", ""])
        return "\n".join(lines)

    process_env = os.environ.copy()
    process_env.update(action.env)

    if action.env:
        env_text = "\n".join(f"{key}={value}" for key, value in sorted(action.env.items()))
        lines.append(
            html_terminal_block(
                "Environment overrides",
                env_text,
                accent="#2563eb",
                header_bg="#eff6ff",
                body_bg="#0f172a",
                text_color="#dbeafe",
            )
        )
        lines.append("")

    command_text = display_paths(shell_quote(action.command))
    command_lines = []
    if action.stdin is None:
        command_lines.append(command_text)
    else:
        command_lines.append(f"{command_text} <<'STDIN'")
        command_lines.append(action.stdin.rstrip())
        command_lines.append("STDIN")
    lines.append(
        html_terminal_block(
            "Executed command",
            "\n".join(command_lines),
            accent="#16a34a",
            header_bg="#f0fdf4",
            body_bg="#052e16",
            text_color="#dcfce7",
        )
    )
    lines.append("")

    result = subprocess.run(
        action.command,
        cwd=ROOT,
        text=True,
        input=action.stdin,
        capture_output=True,
        env=process_env,
    )

    exit_color = "#16a34a" if result.returncode == 0 else "#dc2626"
    lines.append(f'Exit code: <span style="color: {exit_color}; font-weight: 700;">{result.returncode}</span>')
    lines.append("")
    lines.append(
        html_terminal_block(
            "Stdout",
            display_paths(result.stdout),
            accent="#475569",
            header_bg="#f8fafc",
            body_bg="#111827",
            text_color="#e5e7eb",
        )
    )
    lines.append("")

    if result.stderr:
        lines.append(
            html_terminal_block(
                "Stderr",
                display_paths(result.stderr),
                accent="#dc2626",
                header_bg="#fef2f2",
                body_bg="#450a0a",
                text_color="#fee2e2",
            )
        )
        lines.append("")

    return "\n".join(lines)


def build_actions() -> list[Action]:
    py = sys.executable
    actions = [
        Action(
            title="Open the course README",
            description="A new student starts by reading the README start-here instructions.",
            command=[py, "-c", "from pathlib import Path; print(Path('README.md').read_text()[:2200])"],
        ),
        Action(
            title="Validate the course package",
            description="Before learning, confirm the database, scripts, row security, and chatbot smoke tests pass.",
            command=[py, "tests/validate_course.py"],
        ),
        Action(
            title="Lesson 1: Connect to SQLite",
            description="Run the first script to inspect the real database objects and sample student rows.",
            command=[py, "scripts/01_connect_sqlite.py"],
        ),
        Action(
            title="Lesson 2: Pydantic models",
            description="Convert a real SQLite row into a Pydantic model and print a beginner-friendly answer.",
            command=[py, "scripts/02_pydantic_models.py"],
        ),
        Action(
            title="Lesson 3: Query tools",
            description="Run several read-only student database tools.",
            command=[py, "scripts/03_query_tools.py"],
        ),
        Action(
            title="Lesson 4: Optional Pydantic AI summary",
            description="This lesson needs a local Ollama server and a model that can answer from evidence.",
            note="Skipped by default in the recorder so the walkthrough remains deterministic. Run RUN_AI_ACTIONS=1 python tests/record_course_walkthrough.py to include it.",
        ),
        Action(
            title="Lesson 5: CLI routing",
            description="Ask a normal-language question without writing SQL.",
            command=[py, "scripts/05_studentdb_cli.py", "Which students owe money?"],
        ),
        Action(
            title="Final project: student report",
            description="Ask for a student success report by name.",
            command=[py, "final_project/studentdb_assistant.py", "Show me Zara Quinn"],
        ),
        Action(
            title="Final project: incomplete requirements",
            description="Ask for incomplete requirements by EMPLID.",
            command=[py, "final_project/studentdb_assistant.py", "Which requirements are incomplete for 0001012?"],
        ),
        Action(
            title="Row security: advisor can see assigned program",
            description="ADVISOR_COMP can see Computer Science students such as Zara Quinn.",
            command=[py, "final_project/studentdb_assistant.py", "Show me Zara Quinn"],
            env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
        ),
        Action(
            title="Row security: advisor cannot see other program",
            description="ADVISOR_COMP cannot see Business Analytics student Theo Lane.",
            command=[py, "final_project/studentdb_assistant.py", "Show me Theo Lane"],
            env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
        ),
        Action(
            title="Student self-service: own row only",
            description="STUDENT_0001005 can see Zara Quinn.",
            command=[py, "final_project/studentdb_assistant.py", "Show me Zara Quinn"],
            env={"STUDENTDB_OPRID": "STUDENT_0001005"},
        ),
        Action(
            title="Student self-service: another student hidden",
            description="STUDENT_0001005 cannot see Theo Lane.",
            command=[py, "final_project/studentdb_assistant.py", "Show me Theo Lane"],
            env={"STUDENTDB_OPRID": "STUDENT_0001005"},
        ),
        Action(
            title="Conversational agent walkthrough",
            description="Run the terminal chatbot with scripted input and capture the whole conversation.",
            command=[py, "final_project/conversational_studentdb_agent.py"],
            stdin=(
                "Tell me about student 0001005\n"
                "What classes is this student taking?\n"
                "Does this student owe money?\n"
                "Show me Theo Lane\n"
                "exit\n"
            ),
            env={"STUDENTDB_OPRID": "STUDENT_0001005"},
        ),
        Action(
            title="Student self-service stdout capture",
            description="Run the focused transcript generator that writes a plain stdout file.",
            command=[py, "tests/capture_student_self_service_stdout.py"],
        ),
        Action(
            title="Lesson 9: MCP server tool list",
            description="List the MCP tools exposed for compatible AI clients.",
            command=[py, "final_project/studentdb_mcp_server.py", "--list-tools"],
        ),
        Action(
            title="Lesson 9: MCP server smoke test",
            description="Run the deterministic MCP smoke test without starting a blocking server process.",
            command=[py, "final_project/studentdb_mcp_server.py", "--smoke-test"],
        ),
        Action(
            title="Lesson 9: MCP row security smoke test",
            description="Show that the MCP server still respects STUDENTDB_OPRID row security.",
            command=[py, "final_project/studentdb_mcp_server.py", "--smoke-test"],
            env={"STUDENTDB_OPRID": "ADVISOR_COMP"},
        ),
    ]

    if os.getenv("RUN_AI_ACTIONS") == "1":
        actions[5] = Action(
            title="Lesson 4: Optional Pydantic AI summary",
            description="Run the optional Ollama/Pydantic AI evidence-summary lesson.",
            command=[py, "scripts/04_pydantic_ai_summary.py"],
        )

    return actions


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    IMAGE_DIR.mkdir(exist_ok=True)

    lines = [
        "# StudentDB Assistant Course Walkthrough",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "This file records the actions of a new student taking the course.",
        "Each action includes the command, stdout, stderr when present, and exit code.",
        "",
        "## Images",
        "",
        "No images were needed for this terminal-based walkthrough.",
        f"If screenshots are added later, store them under `{IMAGE_DIR.relative_to(ROOT)}/` and link them here.",
        "",
    ]

    for action in build_actions():
        lines.append(run_action(action))

    OUTPUT_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote Markdown walkthrough to {display_paths(str(OUTPUT_FILE))}")


if __name__ == "__main__":
    main()
