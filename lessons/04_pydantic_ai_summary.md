# Lesson 4: Pydantic AI Summary

## 1. Explain The Concept

Pydantic AI creates an `Agent` around a language model. In this course, Python
gets exact database facts first. The AI model only summarizes trusted evidence.

This is important because small local models can omit or change details.

## 2. Full Python Script

Run:

```bash
python scripts/04_pydantic_ai_summary.py
```

Requires Ollama:

```bash
ollama serve
ollama pull llama3.2
export PYDANTIC_AI_MODEL="ollama:llama3.2"
export OLLAMA_BASE_URL="http://localhost:11434/v1"
```

## 3. Step By Step

- Python queries `V_STUDENT_360`, `V_STUDENT_CLASSES`, and `V_STUDENT_BALANCE`.
- The script creates JSON evidence.
- Pydantic AI sends that evidence to Ollama.
- The model writes a short summary.

## 4. Important Functions

- `build_student_evidence()`: deterministic retrieval.
- `summary_agent.run_sync()`: Pydantic AI call.

## 5. Example User Question

```text
Summarize Zara Quinn's academic progress.
```

## 6. Example Assistant Response

```text
Zara Quinn is active in Computer Science, has a 3.91 GPA, and is enrolled in
CS 410. Her balance is -$250.
```

## 7. Common Beginner Mistakes

- Expecting the AI model to be the database.
- Trusting a summary without checking exact evidence.
- Forgetting that `localhost:11434/v1` is an API base, not a browser page.

## 8. Practice

Run the script for Theo Lane and compare the AI summary with the raw evidence.

## Row Security Note

Only pass rows to Pydantic AI after row security has already filtered them. The
model should never receive records that the current operator is not allowed to
see.
