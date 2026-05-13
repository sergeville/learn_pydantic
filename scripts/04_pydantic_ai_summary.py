from __future__ import annotations

import os

from pydantic_ai import Agent

from studentdb_tools import DatabaseDeps, create_student_success_report


os.environ.setdefault("OLLAMA_BASE_URL", "http://localhost:11434/v1")

summary_agent = Agent(
    os.getenv("PYDANTIC_AI_MODEL", "ollama:llama3.2"),
    output_type=str,
    model_settings={"temperature": 0},
    system_prompt=(
        "You are a student success assistant. Use only the JSON evidence. "
        "Do not invent records. Preserve balance signs exactly."
    ),
)


if __name__ == "__main__":
    deps = DatabaseDeps()
    report = create_student_success_report(deps, "0001005")
    evidence = report.model_dump_json(indent=2)

    print("Evidence sent to Pydantic AI:")
    print(evidence)

    print("\nAI summary:")
    result = summary_agent.run_sync(
        "Summarize this student record for an advisor. Use only this evidence:\n"
        f"{evidence}"
    )
    print(result.output)
