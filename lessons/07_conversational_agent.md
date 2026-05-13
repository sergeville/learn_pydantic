# Lesson 7: Conversational StudentDB Agent

## 1. Explain The Concept

The earlier final project answered one question at a time. A conversational
agent keeps running in the terminal until you type `exit`.

The new script is:

```text
final_project/conversational_studentdb_agent.py
```

It includes two modes:

- Safe local mode: fast deterministic database tools. This is the default.
- Pydantic AI tool mode: real `@agent.tool` functions. Enable it with
  `STUDENTDB_AGENT_MODE=tools`.

Why two modes? Local `llama3.2` is useful for summaries, but it is not reliable
enough for strict tool-calling in this project. A stronger tool-capable model can
use the Pydantic AI tools directly.

## 2. Full Python Script

Run the chatbot:

```bash
python final_project/conversational_studentdb_agent.py
```

Try:

```text
Tell me about student 0001005
What classes is this student taking?
Does this student owe money?
Summarize this student for an advisor.
exit
```

Try Pydantic AI tool mode:

```bash
STUDENTDB_AGENT_MODE=tools python final_project/conversational_studentdb_agent.py
```

## 3. Step By Step

The script does the following:

1. Loads the real database path from `scripts/studentdb_tools.py`.
2. Creates `ConversationDeps`, which stores the database and current selected
   student.
3. Creates a Pydantic AI `Agent`.
4. Registers tools with `@studentdb_agent.tool`.
5. Starts a `while True` chat loop.
6. Reads user input.
7. Answers with database evidence.
8. Stops when the user types `exit`.

## 4. Important Functions

### `ConversationDeps`

Stores shared conversation state:

```python
@dataclass
class ConversationDeps:
    database: DatabaseDeps
    current_emplid: str | None = None
    current_student_name: str | None = None
```

This is how the assistant understands follow-up questions like:

```text
What classes is this student taking?
```

### `select_student`

Finds a student by name or EMPLID and remembers that student.

### `get_student_classes_tool`

Uses `V_STUDENT_CLASSES` to answer class-enrollment questions.

### `get_student_balance_tool`

Uses `V_STUDENT_BALANCE`. It preserves signs:

- positive balance: student owes money
- negative balance: student has a credit / institution owes the student

### `create_student_success_report_tool`

Combines profile, classes, balance, holds, checklist items, incomplete
requirements, and financial aid.

### `chat_loop`

Keeps asking for input:

```python
while True:
    user_text = input("\nUser: ").strip()
    if user_text.lower() in {"exit", "quit"}:
        break
```

## 5. Example User Question

```text
User: Tell me about student 0001005.
```

## 6. Example Assistant Response

```text
Agent: Advisor summary for Zara Quinn (0001005):
- Program: Computer Science
- GPA: 3.91
- Balance: -$250
- Holds: 0
- Incomplete requirements: 3
Tools used: create_student_success_report_tool
```

Follow-up:

```text
User: What classes is this student taking?
```

Response:

```text
Agent: Zara Quinn is enrolled in:
- CS 101: Intro to Programming
- CS 220: Data Structures
- CS 330: Databases and Knowledge Graphs
- CS 410: AI Systems Lab
Tools used: get_student_classes_tool
```

## 7. Common Beginner Mistakes

- Expecting a browser page at `localhost:11434/v1`. That is an API base URL.
- Assuming every local model supports reliable tool calling.
- Forgetting to type `exit` to leave the chat loop.
- Asking “this student” before selecting a student.
- Letting the model guess instead of using database tools.

## 8. Practice Exercise

Add a new conversational route/tool for:

```text
Which students have financial aid?
```

Use the real table `CS_FA_AWARD`.

## Row Security Note

The conversational agent has a tool named `inspect_row_security`. It can explain
the current operator's mock security profile. You can test the chatbot with:

```bash
export STUDENTDB_OPRID=ADVISOR_LIMITED
python final_project/conversational_studentdb_agent.py
```

Then ask about Zara Quinn and Orion Reed. Zara should be visible; Orion should
not be visible to `ADVISOR_LIMITED`.
